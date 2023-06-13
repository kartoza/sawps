import axios from "axios";
import ContextLayerInterface from '../../../models/ContextLayer';
import ParcelInterface from '../../../models/Parcel';

const SEARCH_PARCEL_URL = '/api/map/search/parcel/'

/**
 * Determine layer visibility based on selected context layers
 * @param source_layer 
 * @param contextLayers 
 * @returns 
 */
export const checkLayerVisibility = (source_layer: string, contextLayers: ContextLayerInterface[]): boolean => {
    const contextLayer = contextLayers.find(element => element.layer_names && element.layer_names.includes(source_layer))
    if (contextLayer) {
      return contextLayer.isSelected
    }  
    return true
}

/**
 * Render parcel layers for selection
 * @param map 
 * @param layer_names 
 */
export const renderHighlightParcelLayers = (map: maplibregl.Map, layer_names: string[]) => {
    for (let _idx = 0; _idx < layer_names.length; ++_idx) {
        let _layer_name = `${layer_names[_idx]}-select-parcel`
        if (typeof map.getLayer(_layer_name) === 'undefined') {
            map.addLayer({
                'id': _layer_name,
                'type': 'fill',
                'source': 'sanbi',
                'source-layer': `${layer_names[_idx]}`,
                'layout': {},
                'paint': {
                'fill-color': '#F9A95D',
                'fill-opacity': 0.4
                }
            }, 'erf');
        }
        if (typeof map.getLayer(`${_layer_name}-line`) === 'undefined') {
            // add line color
            map.addLayer({
                'id': `${_layer_name}-line`,
                'type': 'line',
                'source': 'sanbi',
                'source-layer': `${layer_names[_idx]}`,
                'layout': {},
                'paint': {
                'line-color': '#FF0000',
                'line-width': [
                    'case',
                    ['boolean', ['feature-state', 'parcel-selected'], false], 4,
                    0
                ]
                }
            });
        }    
    }
}

/**
 * Remove parcel layers when exits parcel selection mode
 * @param map 
 * @param layer_names 
 */
export const removeHighlightParcelLayers = (map: maplibregl.Map, layer_names: string[]) => {
    for (let _idx = 0; _idx < layer_names.length; ++_idx) {
        let _layer_name = `${layer_names[_idx]}-select-parcel`
        let _layer = map.getLayer(_layer_name)
        if (typeof _layer !== 'undefined') {
            map.removeLayer(_layer_name)
        }
        _layer = map.getLayer(`${_layer_name}-line`)
        if (typeof _layer !== 'undefined') {
            map.removeLayer(`${_layer_name}-line`)
        }
    }
}

/**
 * Find context layer from Cadastral boundaries: erf, farm_portion, holding, and parent_farm
 * @param contextLayers 
 * @returns 
 */
export const findParcelLayer = (contextLayers: ContextLayerInterface[]): ContextLayerInterface => {
    return contextLayers.find((element) => element.name.toLowerCase() === 'cadastral boundaries')
}

/**
 * Search parcel by coordinate
 * Note: LngLat is in srid 4326
 * @param lngLat 
 * @param callback 
 */
export const searchParcel = (lngLat: maplibregl.LngLat, callback: (parcel: ParcelInterface) => void) => {
    axios.get(SEARCH_PARCEL_URL + `?lat=${lngLat.lat}&lng=${lngLat.lng}`).then((response) => {
        if (response.data) {
            callback(response.data as ParcelInterface)
        } else {
            callback(null)
        }
    }).catch((error) => {
        callback(null)
    })
}
