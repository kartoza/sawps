import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import ContextLayerInterface, {ContextLayerVisibilityPayload} from '../models/ContextLayer';

export interface LayerFilterInterface {
    contextLayers: ContextLayerInterface[];
}

const initialState: LayerFilterInterface = {
    contextLayers: []
}

export const LayerFilterSlice = createSlice({
    name: 'LayerFilter',
    initialState,
    reducers: {
        setContextLayers: (state, action: PayloadAction<ContextLayerInterface[]>) => {
            state.contextLayers = [...action.payload]
        },
        setSelectedLayers: (state, action: PayloadAction<number[]>) => {
            let _layers = state.contextLayers.map((layer) => {
                if (action.payload.includes(layer.id)) {
                    layer.isSelected = true
                } else {
                    layer.isSelected = false
                }
                return layer
            })
            state.contextLayers = [..._layers]
        },
        toggleLayer: (state, action: PayloadAction<number>) => {
            let _layers = state.contextLayers.map((layer) => {
                if (action.payload === layer.id) {
                    layer.isSelected = !layer.isSelected
                }
                return layer
            })
            state.contextLayers = [..._layers]
        },
        toggleExpandedLayer: (state, action: PayloadAction<number>) => {
            let _layers = state.contextLayers.map((layer) => {
                if (action.payload === layer.id) {
                    layer.isExpanded = !layer.isExpanded
                }
                return layer
            })
            state.contextLayers = [..._layers]
        },
        setLayerVisibility: (state, action: PayloadAction<ContextLayerVisibilityPayload>) => {
            let _layers = state.contextLayers.map((layer) => {
                if (action.payload.id === layer.id) {
                    layer.isSelected = action.payload.isVisible
                }
                return layer
            })
            state.contextLayers = [..._layers]
        }
    }
})

export const {
    setContextLayers,
    setSelectedLayers,
    toggleLayer,
    toggleExpandedLayer,
    setLayerVisibility
} = LayerFilterSlice.actions

export default LayerFilterSlice.reducer;