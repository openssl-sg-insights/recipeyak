import React from "react"
import { NavLink } from "react-router-dom"

import { Loader } from "@/components/Loader"
import { Link } from "@/components/Routing"
import { useDispatch, useSelector } from "@/hooks"
import { Invites } from "@/pages/team-list/Invites"
import { teamsFrom } from "@/store/mapState"
import { fetchingTeamsAsync } from "@/store/thunks"
import { teamURL } from "@/urls"
import { isFailure, isInitial, isLoading, Loading, Success } from "@/webdata"

function useTeams() {
  const dispatch = useDispatch()
  React.useEffect(() => {
    void fetchingTeamsAsync(dispatch)()
  }, [dispatch])
  const loading = useSelector(
    (s) => s.teams.status === "loading" || s.teams.status === "initial",
  )
  const teams = useSelector(teamsFrom)
  if (loading) {
    return Loading()
  }
  return Success(teams)
}

function TeamsList() {
  const teams = useTeams()
  if (isLoading(teams) || isInitial(teams)) {
    return <Loader />
  }

  if (isFailure(teams)) {
    return <p>failure loading</p>
  }

  if (teams.data.length === 0) {
    return <p className="text-muted text-small align-self-center">No teams.</p>
  }

  return (
    <div className="text-left">
      {teams.data.map(({ id, name }) => (
        <p key={id}>
          <NavLink to={teamURL(id, name)} activeClassName="fw-500">
            {name}
          </NavLink>
        </p>
      ))}
    </div>
  )
}

export default function TeamsPage() {
  return (
    <div style={{ maxWidth: 800 }} className="mx-auto mw-800">
      <section className="d-flex justify-space-between align-items-center">
        <h2 className="fs-6">Teams</h2>
        <Link to="/t/create" className="mt-1 ">
          Create a Team
        </Link>
      </section>

      <TeamsList />

      <div>
        <h2 className="fs-6">Invites</h2>
        <Invites />
      </div>
    </div>
  )
}
