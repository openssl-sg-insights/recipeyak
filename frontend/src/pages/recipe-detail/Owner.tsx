import React from "react"
import { connect } from "react-redux"
import { Link } from "react-router-dom"

import {
  ButtonLink,
  ButtonPrimary,
  ButtonSecondary,
} from "@/components/Buttons"
import { Select } from "@/components/Forms"
import GlobalEvent from "@/components/GlobalEvent"
import { isOk, Result } from "@/result"
import { IRecipe } from "@/store/reducers/recipes"
import { ITeamsState } from "@/store/reducers/teams"
import { IUser, IUserState } from "@/store/reducers/user"
import { IState } from "@/store/store"
import {
  copyRecipeToAsync,
  Dispatch,
  fetchingTeamsAsync,
  INotificationWithTimeout,
  moveRecipeToAsync,
  showNotificationWithTimeoutAsync,
} from "@/store/thunks"
import { teamURL } from "@/urls"
import { notUndefined } from "@/utils/general"

function getTeamUserKeys(
  teams: ITeamsState,
  userId: IUser["id"] | null,
): ReadonlyArray<{ id: string; name: string }> {
  return teams.allIds
    .map((id) => {
      const team = teams.byId[id]
      if (team == null) {
        return
      }
      return {
        id: String(id) + "-team",
        name: team.name,
      }
    })
    .filter(notUndefined)
    .concat({ id: String(userId) + "-user", name: "personal" })
}

const mapStateToProps = (state: IState) => ({
  teams: state.teams,
  userId: state.user.id,
})

const mapDispatchToProps = (dispatch: Dispatch) => ({
  fetchData: fetchingTeamsAsync(dispatch),
  showNotificationWithTimeout: showNotificationWithTimeoutAsync(dispatch),
  moveRecipeTo: moveRecipeToAsync(dispatch),
  copyRecipeTo: copyRecipeToAsync(dispatch),
})

interface IOwnerProps {
  readonly fetchData: () => void
  readonly copyRecipeTo: (
    recipeId: IRecipe["id"],
    id: IRecipe["owner"]["id"],
    type: IRecipe["owner"]["type"],
  ) => Promise<void>
  readonly moveRecipeTo: (
    recipeId: IRecipe["id"],
    id: IRecipe["owner"]["id"],
    type: IRecipe["owner"]["type"],
  ) => Promise<Result<void, void>>
  readonly showNotificationWithTimeout: (
    props: INotificationWithTimeout,
  ) => void
  readonly recipeId: IRecipe["id"]
  readonly id: IRecipe["owner"]["id"]
  readonly name: string
  readonly teams: ITeamsState
  readonly userId: IUserState["id"]
}

interface IOwnerState {
  readonly show: boolean
  readonly values: string[]
}

class Owner extends React.Component<IOwnerProps, IOwnerState> {
  state: IOwnerState = {
    show: false,
    values: [],
  }

  dropdown = React.createRef<HTMLSpanElement>()

  componentDidMount() {
    this.props.fetchData()
  }

  handleGeneralClick = (e: MouseEvent) => {
    const el = this.dropdown.current
    if (el == null) {
      return
    }

    const target = e.target
    if (target == null) {
      return
    }

    /* eslint-disable-next-line @typescript-eslint/consistent-type-assertions */
    const clickedDropdown = el.contains(target as HTMLElement)

    if (clickedDropdown) {
      return
    }
    // clear values when closing dropdown
    this.setState({ show: false, values: [] })
  }

  handleChange = (ev: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedOptions = [...ev.target.selectedOptions].map(
      (opt) => opt.value,
    )
    this.setState({ values: selectedOptions })
  }

  toggle = () => {
    this.setState((prev) => {
      if (prev.show) {
        // clear values when closing dropdown
        return { ...prev, show: !prev.show, values: [] }
      }
      return { ...prev, show: !prev.show }
    })
  }

  copy() {
    const [id, type] = this.state.values[0].split("-")
    if (id == null || type == null) {
      return new TypeError("need id/type to move to")
    }
    if (type !== "team" && type !== "user") {
      return new TypeError("type can only either be a team or a user")
    }
    void this.props
      .copyRecipeTo(this.props.recipeId, parseInt(id, 10), type)
      .then(() => {
        this.setState({ show: false, values: [] })
      })
  }

  move() {
    const [id, type] = this.state.values[0].split("-")
    if (id == null || type == null) {
      return new TypeError("need id/type to copy to")
    }
    if (type !== "team" && type !== "user") {
      return new TypeError("type can only either be a team or a user")
    }

    void this.props
      .moveRecipeTo(this.props.recipeId, parseInt(id, 10), type)
      .then((res) => {
        if (isOk(res)) {
          this.setState({ show: false, values: [] })
        } else {
          this.props.showNotificationWithTimeout({
            message: `Problem moving recipe: ${res.error}`,
            level: "danger",
            sticky: true,
          })
        }
      })
  }

  disableMove() {
    return this.state.values.length !== 1
  }

  disableCopy() {
    return this.state.values.length !== 1
  }

  render() {
    const { name, teams, userId } = this.props
    const { moving, copying } = teams

    const teamUserKeys = getTeamUserKeys(teams, userId)

    const url = teamURL(this.props.id, this.props.name)

    return (
      <span className="fw-500 p-rel" ref={this.dropdown}>
        <GlobalEvent mouseUp={this.handleGeneralClick} />
        <span
          className="cursor-pointer"
          title="click to edit"
          onClick={this.toggle}
        >
          via
        </span>{" "}
        <Link to={url}>{name}</Link>
        <div className={"" + (this.state.show ? " d-block" : " d-none")}>
          <div className="p-abs">
            <div className="dropdown-content">
              <div className="text-center">Teams</div>
              <hr className="dropdown-divider mt-1 mb-1" />
              <Select
                multiple
                noBorder
                value={this.state.values}
                onChange={this.handleChange}
                className="max-height-25vh overflow-y-scroll w-100"
              >
                {teamUserKeys.map((opt) => (
                  <option
                    className="text-small fw-500"
                    key={opt.id}
                    value={opt.id}
                  >
                    {opt.name}
                  </option>
                ))}
              </Select>
              <hr className="dropdown-divider" />
              <div className="d-flex justify-space-between ml-2 mr-2">
                <ButtonLink size="small" onClick={this.toggle}>
                  cancel
                </ButtonLink>
                <div className="d-flex justify-space-between">
                  <ButtonSecondary
                    size="small"
                    loading={moving}
                    className="mr-1"
                    onClick={() => this.move()}
                    disabled={this.disableMove()}
                  >
                    move
                  </ButtonSecondary>
                  <ButtonPrimary
                    size="small"
                    loading={copying}
                    onClick={() => this.copy()}
                    disabled={this.disableCopy()}
                  >
                    copy
                  </ButtonPrimary>
                </div>
              </div>
            </div>
          </div>
        </div>
      </span>
    )
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Owner)
