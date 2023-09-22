import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import SpeciesLayer from "../models/SpeciesLayer";

export interface SpeciesFilterInterface {
  SpeciesFilterList: SpeciesLayer[];
  selectedSpecies: string;
  months: string[];
  selectedMonths: string;
  startYear: number;
  endYear: number;
  propertyId:string;
  selectedInfoList: string;
  organisationId:string;
}

const initialState: SpeciesFilterInterface = {
  SpeciesFilterList: [],
  selectedSpecies: "",
  months: [],
  selectedMonths: "",
  startYear: 1960,
  endYear:new Date().getFullYear(),
  propertyId:"",
  selectedInfoList:"",
  organisationId:"",
};

export const SpeciesFilterSlice = createSlice({
  name: 'SpeciesFilter',
  initialState,
  reducers: {
    setSpeciesFilter: (state, action: PayloadAction<SpeciesLayer[]>) => {
      state.SpeciesFilterList = [...action.payload];

      const selectedSpecies = action.payload
        .filter(obj => obj.is_selected)
        .map(obj => obj.common_name_varbatim);
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
        .map(obj => obj.common_name_varbatim);
      state.selectedSpecies = selectedSpecies.join(',');
    },
    toggleSpecies: (state, action: PayloadAction<string>) => {
      state.selectedSpecies = action.payload;
    },
    setSelectedInfoList: (state, action: PayloadAction<string>) => {
      state.selectedInfoList = action.payload;
    },

    selectedPropertyId: (state, action: PayloadAction<string>) => {
      state.propertyId = action.payload;
    },

    selectedOrganisationId: (state, action: PayloadAction<string>) => {
      state.propertyId = action.payload;
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
  },
});

export const {
  setSpeciesFilter,
  toggleSpecies,
  setSelectedSpecies,
  selectedPropertyId,
  selectedOrganisationId,
  setMonths,
  setStartYear,
  setEndYear,
  setSelectedInfoList,
} = SpeciesFilterSlice.actions;

export default SpeciesFilterSlice.reducer;
