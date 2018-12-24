import * as React from "react"
import { MemoryRouter } from "react-router"

import { mount, configure } from "enzyme"
import Adapter from "enzyme-adapter-react-16"

import { Provider } from "react-redux"
import { emptyStore as store } from "../store/store"

import Home from "./Home"

configure({ adapter: new Adapter() })

describe("<Home/>", () => {
  it("renders without crashing", () => {
    mount(
      <Provider store={store}>
        <MemoryRouter>
          <Home loggedIn={false} />
        </MemoryRouter>
      </Provider>
    )
  })
  it("Has some text in footer", () => {
    const home = mount(
      <Provider store={store}>
        <MemoryRouter>
          <Home loggedIn={false} />
        </MemoryRouter>
      </Provider>
    )
    expect(
      home
        .find("a")
        .first()
        .text()
    ).toContain("Create Account")
  })
})