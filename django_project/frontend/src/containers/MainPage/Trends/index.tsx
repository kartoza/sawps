import React, { useEffect, useState } from "react";
import {Box, Button, Checkbox, Grid, ListItemText, Typography} from "@mui/material";
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import Loading from '../../../components/Loading';
import { saveAs } from 'file-saver';
import * as XLSX from 'xlsx';
import axios from "axios";
import { useAppSelector } from "../../../app/hooks";
import { RootState } from "../../../app/store";
import { getTitle } from "../../../utils/Helpers";
import {
    Activity,
    useGetUserInfoQuery,
    useGetActivityAsObjQuery,
    UserInfo
} from "../../../services/api";
import Topper from "./Topper";

import OverviewCardsHolder from '../../../components/LandingPage/LandingPagePopulationOverview/OverviewCardsHolder'
import './index.scss';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250,
        },
    },
};

const FETCH_GRAPH_SPECIES_LIST = '/api/species/front-page/list/'

const DataList = () => {

    return (
      <Box>
          <h1>Trends Page</h1>
      </Box>
    )
}

export default DataList
