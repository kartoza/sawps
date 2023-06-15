import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import ParcelInterface from "../models/Parcel";
import { MapSelectionMode, MapEventInterface } from "../models/Map";
import PropertyInterface, { createNewProperty } from "../models/Property";

const DEFAULT_SELECTION_MODE = MapSelectionMode.Property


export interface MapStateInterface {
    isMapReady: boolean;
    selectionMode: MapSelectionMode; // none, property, parcel, digitise, parcelJSON,
    selectedParcels: ParcelInterface[];
    selectedProperty: PropertyInterface;
    mapEvents: MapEventInterface[];
}

const initialState: MapStateInterface = {
    isMapReady: false,
    selectionMode: DEFAULT_SELECTION_MODE,
    selectedParcels: [],
    selectedProperty: createNewProperty(),
    mapEvents: []
}

/* reset all selectedParcels */
const resetSelectedParcels = (parcels: ParcelInterface[]): ParcelInterface[] => {
    let _selection = [...parcels]
    _selection.forEach(function(item, index, object) {
        item.isRemoved = true
    })
    return _selection
}


export const MapStateSlice = createSlice({
    name: 'MapState',
    initialState,
    reducers: {
        setMapReady: (state, action: PayloadAction<boolean>) => {
            state.isMapReady = action.payload
        },
        toggleParcelSelectionMode: (state, action: PayloadAction<null>) => {
            // reset selectedProperty
            state.selectedProperty = createNewProperty()
            if (state.selectionMode === MapSelectionMode.Parcel) {
                // disable parcel selection mode
                state.selectionMode = DEFAULT_SELECTION_MODE
                // remove selectedParcels
                state.selectedParcels = resetSelectedParcels(state.selectedParcels)
            } else {
                state.selectionMode = MapSelectionMode.Parcel
            }
        },
        toggleParcelSelectedState: (state, action: PayloadAction<ParcelInterface>) => {
            let _idx = state.selectedParcels.findIndex((element) => element.id === action.payload.id && element.layer === action.payload.layer)
            if (_idx > -1) {
                // remove selection
                let _selection = [...state.selectedParcels]
                _selection[_idx].isRemoved = true
                state.selectedParcels = _selection
            } else {
                state.selectedParcels = [...state.selectedParcels, action.payload]
            }
        },
        setSelectedProperty: (state, action: PayloadAction<PropertyInterface>) => {
            state.selectedProperty = {...action.payload}
        },
        resetSelectedProperty: (state, action: PayloadAction<null>) => {
            // reset selectedProperty
            state.selectedProperty = createNewProperty()
        },
        selectedParcelsOnRenderFinished: (state, action: PayloadAction<null>) => {
            // called when selected parcels have been rendered
            let _selection = [...state.selectedParcels]
            _selection.forEach(function(item, index, object) {
                if (item.isRemoved) {
                  object.splice(index, 1);
                }
            })
            state.selectedParcels = _selection
        },
        triggerMapEvent: (state, action: PayloadAction<MapEventInterface>) => {
            state.mapEvents = [...state.mapEvents, action.payload]
        },
        onMapEventProcessed: (state, action: PayloadAction<MapEventInterface[]>) => {
            let _events = [...state.mapEvents]
            _events.forEach(function(item, index, object) {
                if (action.payload.find((e: MapEventInterface) => e.id === item.id)) {
                    object.splice(index, 1)
                }
            })
            state.mapEvents = _events
        }
    }
})

export const {
    setMapReady,
    toggleParcelSelectionMode,
    toggleParcelSelectedState,
    setSelectedProperty,
    resetSelectedProperty,
    selectedParcelsOnRenderFinished,
    triggerMapEvent,
    onMapEventProcessed
} = MapStateSlice.actions

export default MapStateSlice.reducer;