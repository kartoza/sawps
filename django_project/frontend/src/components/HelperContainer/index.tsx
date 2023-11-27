import React, { ReactElement, useState } from "react";
import { DocsCrawlerPage } from "django-docs-crawler-react";
import HelpCenterIcon from '@mui/icons-material/HelpCenter';

import "django-docs-crawler-react/dist/style.css"

interface Interface {
  relativeUrl?: string;
  open: boolean;
  setOpen?: React.Dispatch<React.SetStateAction<boolean>>;
  footer?: ReactElement;
}


export function HelperContainer(props: Interface) {
  return <DocsCrawlerPage
    dataUrl={'/docs_crawler/data'}
    relativeUrl={props.relativeUrl}
    open={props.open}
    setOpen={
      props.setOpen ? props.setOpen : () => {
      }
    }
    footer={props.footer}
  />;
}

interface TogglerInterface {
  relativeUrl?: string;
}

export function HelperContainerWithToggle(props: TogglerInterface) {
  const [open, setOpen] = useState(false)
  return <>
    <HelperContainer
      open={open}
      relativeUrl={props.relativeUrl}
      setOpen={setOpen}
    />
    <HelpCenterIcon
      style={{
        cursor: "pointer",
        marginLeft: "auto",
        color: "var(--green-darken-1)"
      }}
      onClick={() => setOpen(true)}
    />
  </>
}
