import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import ContextLayerInterface, {ContextLayerVisibilityPayload, NGI_AERIAL_IMAGERY_LAYER, NGI_LAYER_GROUP} from '../models/ContextLayer';

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
            let _payloadLayers = state.contextLayers.filter(a => a.id === action.payload)
            let _foundLayer: ContextLayerInterface = null;
            if (_payloadLayers.length) {
                _foundLayer = {..._payloadLayers[0]}
            }
            console.log('foundLayer : ', _foundLayer)
            let _layers = state.contextLayers.map((layer) => {
                if (_foundLayer && _foundLayer.name === NGI_AERIAL_IMAGERY_LAYER) {
                    if (!_foundLayer.isSelected) {
                        // enable NGI Aerial Image and Properties
                        if (NGI_LAYER_GROUP.includes(layer.name)) {
                            layer.isSelected = true
                        } else {
                            layer.isSelected = false
                        }
                    } else {
                        // disable NGI Aerial Image and enable the rest
                        if (layer.name === NGI_AERIAL_IMAGERY_LAYER) {
                            layer.isSelected = false
                        } else {
                            layer.isSelected = true
                        }
                    }                    
                } else {
                    if (action.payload === layer.id) {
                        layer.isSelected = !layer.isSelected
                    }
                }
                console.log('layer name: ', layer.name, layer.isSelected)
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