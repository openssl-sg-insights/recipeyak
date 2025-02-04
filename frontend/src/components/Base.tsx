import React from "react"

import ErrorBoundary from "@/components/ErrorBoundary"
import Footer from "@/components/Footer"
import { Navbar } from "@/components/Nav"

export const ContainerBase = ({ children }: { children: React.ReactNode }) => (
  <>
    <Navbar />
    <ErrorBoundary>{children}</ErrorBoundary>
  </>
)

export const Container = ({ children }: { children: React.ReactNode }) => (
  <>
    <div className="pb-3 pt-0 container w-100 pl-3 pr-3">
      <ErrorBoundary>{children}</ErrorBoundary>
    </div>
    <Footer />
  </>
)

export default Container
