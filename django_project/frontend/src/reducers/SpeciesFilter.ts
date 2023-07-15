import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import SpeciesLayer from "../models/SpeciesLayer";

export interface SpeciesFilterInterface {
    SpeciesFilterList: SpeciesLayer[];
    months: string[];
    startYear: number;
    endYear: number;
}

const initialState: SpeciesFilterInterface = {
    SpeciesFilterList: [],
    months: [],
    startYear: 1960,
    endYear: 2023,
}

export const SpeciesFilterSlice = createSlice({
    name: 'SpeciesFilter',
    initialState,
    reducers: {
        setSpeciesFilter: (state, action: PayloadAction<SpeciesLayer[]>) => {
            state.SpeciesFilterList = [...action.payload]
        },
        setSelectedSpecies: (state, action: PayloadAction<number[]>) => {
            let _updatedData = state.SpeciesFilterList.map((species) => {
                if (action.payload.includes(species.id)) {
                    species.is_selected = true
                } else {
                    species.is_selected = false
                }
                return species
            })
            state.SpeciesFilterList = [..._updatedData]
        },
        toggleSpecies: (state, action: PayloadAction<number>) => {
            const _updatedData = state.SpeciesFilterList.map((species) => {
                if (action.payload === species.id) {

                    species.is_selected = !species.is_selected
                }
                return species;
            });
            state.SpeciesFilterList = [..._updatedData]
        },

        setMonths: (state, action: PayloadAction<string[]>) => {
            state.months = [...action.payload];
        },

        setStartYear: (state, action: PayloadAction<number>) => {
            state.startYear = action.payload;
          },

        setEndYear: (state, action: PayloadAction<number>) => {
            state.endYear = action.payload;
          },
    }
})

export const {
    setSpeciesFilter,
    toggleSpecies,
    setSelectedSpecies,
    setMonths,
    setStartYear,
    setEndYear
} = SpeciesFilterSlice.actions

export default SpeciesFilterSlice.reducer;