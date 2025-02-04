import { IState } from "@/store/store"

/** JSONParse that doesn't throw
 *
 * Returning errors instead of throwing is better because TS ensures that we
 * handle this error case.
 */
const jsonParse = <T>(text: string) => {
  // We need to use a try here to allow us to return an error

  try {
    /* eslint-disable @typescript-eslint/consistent-type-assertions */
    return JSON.parse(text) as T
  } catch (err) {
    // This is a lie, but it's an acceptable one
    return err as SyntaxError
    /* eslint-enable @typescript-eslint/consistent-type-assertions */
  }
}

export const loadState = () => {
  const serializedState = localStorage.getItem("state")
  if (serializedState === null) {
    return undefined
  }
  return jsonParse<Partial<IState>>(serializedState)
}

export const saveState = (state: IState) => {
  const serializedState = JSON.stringify(state)
  localStorage.setItem("state", serializedState)
}
