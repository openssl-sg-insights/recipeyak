interface ILogoProps {
  readonly light?: boolean
  readonly width?: string
}

export function Logo({ light = false, width = "50px" }: ILogoProps) {
  return (
    <svg
      className={`mr-1 ${light ? "fill-white" : "fill-text-color"} `}
      width={width}
      viewBox="0 0 512 512"
      version="1.1"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M436.6,87.8c-0.9,0.1-1.9,2.7-3.7,7.9c-2.8,8.1-4.3,14.3-5.2,18.3c-1.4,5.6-3,12.1-5.2,18.8c-2.7,7.9-4.2,12.5-7.7,18.2
        c-4,6.3-8.2,10.6-10.6,13c-2.7,2.7-8,7.5-15.8,12.3c-4.9,3-12.4,6.9-22.3,10c-8.9,2.7-16.9,4.6-24.2,5.9c-2.8,0.5-7.5,1.3-16.4,2.3
        c-5.3,0.6-19.8,2.1-43.9,2.9c-6.7,0.2-15.4,0.4-25.6,0.5c-10.2,0-18.9-0.3-25.6-0.5c-24-0.8-38.5-2.3-43.9-2.9
        c-8.9-1-13.5-1.7-16.4-2.3c-7.3-1.3-15.3-3.2-24.2-5.9c-9.9-3-17.3-6.9-22.3-10c-7.8-4.8-13.1-9.6-15.8-12.3
        c-2.4-2.4-6.6-6.6-10.6-13c-3.6-5.7-5.1-10.3-7.7-18.2c-2.3-6.6-3.8-13.2-5.2-18.8c-1-4-2.4-10.2-5.2-18.3c-1.8-5.2-2.8-7.9-3.7-7.9
        c-4.1-0.3-13.2,23.2-12.1,47.4c0.3,7.5,1.4,25.9,14.4,44.9c10.2,14.8,23.4,23.8,31.6,29.4c10.6,7.2,14.1,7.4,19.7,11.5
        c12.4,9.2,14.8,20.5,22.4,60c6,30.9,11.1,64,22,95.4c2.5,7.3,6.6,27.5,22.5,40.9c7.4,6.2,16.6,10.8,16.6,10.8
        c3.2,1.6,11.6,5.5,23.4,7.8c7.4,1.4,14.1,1.9,20.1,1.8c5.9,0.1,12.7-0.4,20.1-1.8c11.8-2.3,20.2-6.2,23.4-7.8c0,0,9.2-4.6,16.6-10.8
        c15.9-13.4,20-33.6,22.5-40.9c10.9-31.4,16-64.5,22-95.4c7.6-39.6,10.1-50.9,22.4-60c5.6-4.1,9.1-4.3,19.7-11.5
        c8.2-5.6,21.4-14.5,31.6-29.4c13-19,14.1-37.4,14.4-44.9C449.7,110.9,440.6,87.5,436.6,87.8z M333.2,258.7
        c-7.1,53.7-13.8,82-24.6,107.8c-0.4,1.1-1.3,3.3-2.9,6.1c-5.1,9.2-13.1,24.4-31,30.8c-18.3,6.6-36.3,0.3-37.3,0
        c-17.9-6.4-25.9-21.6-31-30.8c-1.6-2.8-2.5-5.1-2.9-6.1c-10.8-25.7-17.5-54.1-24.6-107.8c-1.3-10.1-2.3-18,3.7-22.9
        c6.5-5.3,15.5-4,38.4-3.2c20.4,0.7,49.6,0.7,70,0c23-0.8,31.9-2.1,38.4,3.2C335.4,240.7,334.5,248.6,333.2,258.7z"
      />
    </svg>
  )
}

export default Logo
