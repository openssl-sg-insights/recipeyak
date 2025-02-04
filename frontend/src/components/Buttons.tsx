import * as React from "react"

import { assertNever } from "@/assert"
import { classNames } from "@/classnames"

export const ButtonLink = (props: IButtonProps) => (
  <ButtonPlain {...props} className={classNames(props.className, "is-link")} />
)

export const ButtonPrimary = (props: IButtonProps) => (
  <ButtonPlain
    {...props}
    className={classNames(props.className, "is-primary")}
  />
)

export const ButtonDanger = (props: IButtonProps) => (
  <ButtonPlain
    {...props}
    className={classNames(props.className, "is-danger")}
  />
)

export const ButtonSecondary = (props: IButtonProps) => (
  <ButtonPlain
    {...props}
    className={classNames(props.className, "is-secondary")}
  />
)

interface IButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  readonly loading?: boolean
  readonly size?: "small" | "normal"
}
export const ButtonPlain = ({
  loading = false,
  className = "",
  size = "normal",
  children,
  ...props
}: IButtonProps) => {
  const buttonSize =
    size === "small"
      ? "is-small"
      : size === "normal"
      ? "is-normal"
      : assertNever(size)
  return (
    <button
      {...props}
      disabled={loading || props.disabled}
      className={classNames("my-button", "br-6", className, buttonSize, {
        "is-loading": loading,
      })}
    >
      {children}
    </button>
  )
}

export const Button = ButtonPlain
