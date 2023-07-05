import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import SpeciesLayer from "../models/SpeciesLayer";

export interface SpeciesFilterInterface {
    SpeciesFilterList: SpeciesLayer[];
}

const initialState: SpeciesFilterInterface = {
    SpeciesFilterList: []
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
                    species.isSelected = true
                } else {
                    species.isSelected = false
                }
                return species
            })
            state.SpeciesFilterList = [..._updatedData]
        },
        toggleSpecies: (state, action: PayloadAction<number>) => {
            const _updatedData = state.SpeciesFilterList.map((species) => {
                if (action.payload === species.id) {
                    
                    species.isSelected = !species.isSelected
                }
                return species;
              });
            state.SpeciesFilterList = [..._updatedData]
        }
    }
})

export const {
    setSpeciesFilter,
    toggleSpecies,
    setSelectedSpecies,
} = SpeciesFilterSlice.actions

export default SpeciesFilterSlice.reducer;