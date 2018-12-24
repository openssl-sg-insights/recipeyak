import React from "react"
import PropTypes from "prop-types"

import { classNames } from "../classnames"

interface IModalProps {
  readonly onClose: () => void
  readonly className?: string
  readonly show: boolean
}

export default class Modal extends React.Component<IModalProps> {
  static propTypes = {
    onClose: PropTypes.func,
    show: PropTypes.bool.isRequired,
    children: PropTypes.arrayOf(PropTypes.node.isRequired)
  }

  // TODO(sbdchd): remove once everything is typescript
  static defaultProps = {
    onClose: () => undefined,
    className: ""
  }

  componentWillMount() {
    document.addEventListener("keydown", this.handleKeyDown)
  }

  componentWillUnmount() {
    document.removeEventListener("keydown", this.handleKeyDown)
  }

  handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Escape") {
      this.props.onClose()
    }
  }

  close = () => {
    this.props.onClose()
  }

  render() {
    const { show, children } = this.props
    return (
      <div className={classNames("modal", { "is-active": show })}>
        <div className="modal-background" onClick={this.close} />
        <div
          className={`modal-content overflow-y-auto ${this.props.className}`}>
          <div className="box">{children}</div>
        </div>
        <button
          className="modal-close is-large"
          aria-label="close"
          onClick={this.close}
        />
      </div>
    )
  }
}