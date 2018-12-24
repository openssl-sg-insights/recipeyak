import React from "react"
import { MemoryRouter } from "react-router"
import { Provider } from "react-redux"
import { mount, configure } from "enzyme"
import Adapter from "enzyme-adapter-react-16"

import { emptyStore as store } from "../store/store"

import OAuth from "./OAuth"

configure({ adapter: new Adapter() })

describe("<OAuth/>", () => {
  it("renders without crashing", () => {
    mount(
      <Provider store={store}>
        <MemoryRouter>
          <OAuth service="gitlab" token="12345" login={jest.fn()} />
        </MemoryRouter>
      </Provider>
    )
  })
})
