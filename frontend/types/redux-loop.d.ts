/* eslint-disable @typescript-eslint/no-explicit-any */
import {
  Action,
  ActionCreator,
  AnyAction,
  // eslint-disable-next-line no-restricted-imports
  Dispatch,
  Store,
  StoreEnhancer,
} from "redux"

export interface StoreCreator {
  <S, A extends Action>(
    reducer: LoopReducer<S, A>,
    preloadedState: S | undefined,
    enhancer: StoreEnhancer<S>,
  ): Store<S>
}

export type Loop<S, A extends Action> = [S, CmdType<A>]

export interface LoopReducer<S, A extends Action> {
  (state: S | undefined, action: AnyAction, ...args: any[]): S | Loop<S, A>
}

export interface LoopReducerWithDefinedState<S, A extends Action> {
  (state: S, action: AnyAction, ...args: any[]): S | Loop<S, A>
}

export interface LiftedLoopReducer<S, A extends Action> {
  (state: S | undefined, action: AnyAction, ...args: any[]): Loop<S, A>
}

export type CmdSimulation = {
  result: any
  success: boolean
}
export interface MultiCmdSimulation {
  [index: number]: CmdSimulation | MultiCmdSimulation
}

export interface NoneCmd {
  readonly type: "NONE"
  simulate(): null
}

export interface ListCmd<A extends Action> {
  readonly type: "LIST"
  readonly cmds: CmdType<A>[]
  readonly sequence?: boolean
  readonly batch?: boolean
  simulate(simulations: MultiCmdSimulation): A[]
}

export interface ActionCmd<A extends Action> {
  readonly type: "ACTION"
  readonly actionToDispatch: A
  simulate(): A
}

export interface MapCmd<A extends Action> {
  readonly type: "MAP"
  readonly tagger: ActionCreator<A>
  readonly nestedCmd: CmdType<A>
  readonly args: any[]
  simulate(simulations?: CmdSimulation | MultiCmdSimulation): A[] | A | null
}

export interface RunCmd<A extends Action> {
  readonly type: "RUN"
  readonly func: Function
  readonly args?: any[]
  readonly failActionCreator?: ActionCreator<A>
  readonly successActionCreator?: ActionCreator<A>
  readonly forceSync?: boolean
  simulate(simulation: CmdSimulation): A
}

//deprecated types
export type SequenceCmd<A extends Action> = ListCmd<A>
export type BatchCmd<A extends Action> = ListCmd<A>

export type CmdType<A extends Action> =
  | ActionCmd<A>
  | ListCmd<A>
  | MapCmd<A>
  | NoneCmd
  | RunCmd<A>
  | BatchCmd<A>
  | SequenceCmd<A>

export interface LoopConfig {
  readonly DONT_LOG_ERRORS_ON_HANDLED_FAILURES: boolean
}

declare function install<S>(config?: LoopConfig): StoreEnhancer<S>

declare function loop<S, A extends Action>(
  state: S,
  cmd: CmdType<A>,
): Loop<S, A>

type UnwrapPromise<T> = T extends Promise<infer U> ? U : T
type UnwrappedReturn<F> = F extends (...args: any[]) => infer R
  ? UnwrapPromise<R>
  : never

type FunctionArgs<F> = F extends (...args: infer T) => any ? T : never

// see: https://github.com/redux-loop/redux-loop/pull/191/files#diff-b52768974e6bc0faccb7d4b75b162c99R87
type Opaque<K, T> = T & { __TYPE__: K }
type GetState = <T>() => T & Opaque<"GetState", symbol>

declare namespace Cmd {
  export const dispatch: Dispatch & Opaque<"Dispatch", symbol>
  export const getState: GetState

  export const none: NoneCmd
  export function action<A extends Action>(action: A): ActionCmd<A>
  export function batch<A extends Action>(cmds: CmdType<A>[]): BatchCmd<A>
  export function sequence<A extends Action>(cmds: CmdType<A>[]): SequenceCmd<A>

  export function list<A extends Action>(
    cmds: CmdType<A>[],
    options?: {
      batch?: boolean
      sequence?: boolean
      testInvariants?: boolean
    },
  ): ListCmd<A>

  export function map<A extends Action, B extends Action>(
    cmd: CmdType<B>,
    tagger: (subAction: B) => A,
    args?: any[],
  ): MapCmd<A>

  // see: https://github.com/antoinewdg/redux-loop/blob/6e4caeb81e563da84741cb3fad83976ce9c601f3/index.d.ts
  export function run<A extends Action, B extends Action, F extends () => void>(
    f: F,
    options?: {
      failActionCreator?: ActionCreator<A>
      successActionCreator?: (arg: UnwrappedReturn<F>) => B
      forceSync?: boolean
    },
  ): RunCmd<A>

  export function run<A extends Action, B extends Action, F extends Function>(
    f: F,
    options: {
      args: FunctionArgs<F>
      failActionCreator?: ActionCreator<A>
      successActionCreator?: (arg: UnwrappedReturn<F>) => B
      forceSync?: boolean
    },
  ): RunCmd<A>
}

export type ReducerMapObject<S, A extends Action = AnyAction> = {
  [K in keyof S]: LoopReducer<S[K], A>
}

declare function combineReducers<S, A extends Action = AnyAction>(
  reducers: ReducerMapObject<S, A>,
): LiftedLoopReducer<S, A>

declare function mergeChildReducers<S, A extends Action = AnyAction>(
  parentResult: S | Loop<S, A>,
  action: AnyAction,
  childMap: ReducerMapObject<S, A>,
): Loop<S, A>

declare function reduceReducers<S, A extends Action = AnyAction>(
  initialReducer: LoopReducer<S, A>,
  ...reducers: Array<LoopReducerWithDefinedState<S, A>>
): LiftedLoopReducer<S, A>

declare function liftState<S, A extends Action>(
  state: S | Loop<S, A>,
): Loop<S, A>

declare function isLoop(test: any): boolean

declare function getModel<S>(loop: S | Loop<S, AnyAction>): S

declare function getCmd<A extends Action>(a: any): CmdType<A> | null
