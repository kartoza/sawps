import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import SpeciesLayer from "../models/SpeciesLayer";

export interface SpeciesFilterInterface {
  SpeciesFilterList: SpeciesLayer[];
  selectedSpecies: string;
  selectedSpeciesList: string;
  months: string[];
  selectedMonths: string;
  startYear: number;
  endYear: number;
  propertyId:string;
  selectedInfoList: string;
  organisationId:string;
  activityId:string;
  spatialFilterValues: string,
  activityName: string,
  propertyName:string;
  organisationName:string;
  propertyCount:number;
  organisationCount:number;
  activityCount:number;
  selectedProvinceName: string,
  selectedProvinceCount: number,
}

export const DEFAULT_START_YEAR_FILTER = 1960
export const DEFAULT_END_YEAR_FILTER = new Date().getFullYear()

const initialState: SpeciesFilterInterface = {
  SpeciesFilterList: [],
  selectedSpecies: "",
  selectedSpeciesList: "",
  months: [],
  selectedMonths: "",
  startYear: DEFAULT_START_YEAR_FILTER,
  endYear:DEFAULT_END_YEAR_FILTER,
  propertyId:"",
  selectedInfoList:"",
  organisationId:"",
  activityId:"",
  spatialFilterValues: "",
  activityName: "",
  propertyName:"",
  organisationName: "",
  propertyCount: 0,
  organisationCount: 0,
  activityCount: 0,
  selectedProvinceName: "",
  selectedProvinceCount: 0,
};

export const SpeciesFilterSlice = createSlice({
  name: 'SpeciesFilter',
  initialState,
  reducers: {
    setSpeciesFilter: (state, action: PayloadAction<SpeciesLayer[]>) => {
      state.SpeciesFilterList = [...action.payload];

      const selectedSpecies = action.payload
        .filter(obj => obj.is_selected)
        .map(obj => obj.common_name_verbatim);
      state.selectedSpecies = selectedSpecies.join(',');
    },
    setSelectedSpecies: (state, action: PayloadAction<number[]>) => {
      let _updatedData = state.SpeciesFilterList.map((species) => {
        if (action.payload.includes(species.id)) {
          species.is_selected = true;
        } else {
          species.is_selected = false;
        }
        return species;
      });
      state.SpeciesFilterList = [..._updatedData];

      const selectedSpecies = _updatedData
        .filter(obj => obj.is_selected)
        .map(obj => obj.common_name_verbatim);
      state.selectedSpecies = selectedSpecies.join(',');
    },
    toggleSpecies: (state, action: PayloadAction<string>) => {
      state.selectedSpecies = action.payload;
    },
    toggleSpeciesList: (state, action: PayloadAction<string>) => {
      state.selectedSpeciesList = action.payload;
    },
    setSelectedInfoList: (state, action: PayloadAction<string>) => {
      state.selectedInfoList = action.payload;
    },

    selectedPropertyId: (state, action: PayloadAction<string>) => {
      state.propertyId = action.payload;
    },

    selectedOrganisationId: (state, action: PayloadAction<string>) => {
      state.organisationId = action.payload;
    },
    selectedActivityId: (state, action: PayloadAction<string>) => {
      state.activityId = action.payload;
    },
    setMonths: (state, action: PayloadAction<string[]>) => {
      state.months = [...action.payload];
      state.selectedMonths = action.payload.join(',');
    },

    setStartYear: (state, action: PayloadAction<number>) => {
      state.startYear = action.payload;
    },

    setEndYear: (state, action: PayloadAction<number>) => {
      state.endYear = action.payload;
    },
    setSpatialFilterValues: (state, action: PayloadAction<string[]>) => {
      state.spatialFilterValues = action.payload.join(',');
    },
    selectedActivityName: (state, action: PayloadAction<string>) => {
      state.activityName = action.payload;
    },
    selectedPropertyName: (state, action: PayloadAction<string>) => {
      state.propertyName = action.payload;
    },
    selectedOrganisationName: (state, action: PayloadAction<string>) => {
      state.organisationName = action.payload;
    },
    setPropertyCount: (state, action: PayloadAction<number>) => {
      state.propertyCount = action.payload;
    },
    setOrganisationCount: (state, action: PayloadAction<number>) => {
      state.organisationCount = action.payload;
    },
    setActivityCount: (state, action: PayloadAction<number>) => {
      state.activityCount = action.payload;
    },
    setSelectedProvinceCount: (state, action: PayloadAction<number>) => {
      state.selectedProvinceCount = action.payload;
    },
    setSelectedProvinceName: (state, action: PayloadAction<string>) => {
      state.selectedProvinceName = action.payload;
    },
  },
});

export const {
  setSpeciesFilter,
  toggleSpecies,
  toggleSpeciesList,
  setSelectedSpecies,
  selectedPropertyId,
  selectedOrganisationId,
  selectedActivityId,
  setMonths,
  setStartYear,
  setEndYear,
  setSelectedInfoList,
  setSpatialFilterValues,
  selectedActivityName,
  selectedPropertyName,
  selectedOrganisationName,
  setPropertyCount,
  setOrganisationCount,
  setActivityCount,
  setSelectedProvinceCount,
  setSelectedProvinceName
} = SpeciesFilterSlice.actions;

export default SpeciesFilterSlice.reducer;
