import {createSlice, PayloadAction} from "@reduxjs/toolkit";

export interface MapStatusInterface {
    isMapReady: boolean;
}

const initialState: MapStatusInterface = {
    isMapReady: false
}

export const MapStatusSlice = createSlice({
    name: 'MapStatus',
    initialState,
    reducers: {
        setMapReady: (state, action: PayloadAction<boolean>) => {
            state.isMapReady = action.payload
        }
    }
})

export const {
    setMapReady
} = MapStatusSlice.actions

export default MapStatusSlice.reducer;