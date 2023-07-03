import axios from "axios";
import ContextLayerInterface from '../../../models/ContextLayer';
import ParcelInterface from '../../../models/Parcel';
import PropertyInterface from "../../../models/Property";

const SEARCH_PARCEL_URL = '/api/map/search/parcel/'
const SEARCH_PROPERTY_URL = '/api/map/search/property/'
const PARCELS_ORIGINAL_ZOOM_LEVELS: any = {
    'erf': 14,
    'holding': 12,
    'farm_portion': 12,
    'parent_farm': 10
}

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
 * Return all layers for select parcels
 * @param layer_names 
 * @returns 
 */
export const getSelectParcelLayerNames = (layer_names: string[]) => {
    let _results: string[] = []
    for (let _idx = 0; _idx < layer_names.length; ++_idx) {
        let _layer_name = `${layer_names[_idx]}-select-parcel`
        _results.push(_layer_name)
    }
    return _results
}

/**
 * Render parcel layers for selection
 * @param map 
 * @param layer_names 
 */
export const renderHighlightParcelLayers = (map: maplibregl.Map, layer_names: string[]) => {
    for (let _idx = 0; _idx < layer_names.length; ++_idx) {
        if (layer_names[_idx].indexOf('_labels') > -1) continue
        // parent_farm will not be in select mode because it is broken down to smaller parcels (farm_portions)
        if (layer_names[_idx].indexOf('parent_farm') > -1) continue
        let _layer_name = `${layer_names[_idx]}-select-parcel`
        if (typeof map.getLayer(_layer_name) === 'undefined') {
            map.addLayer({
                'id': _layer_name,
                'type': 'fill',
                'source': 'sanbi',
                'source-layer': `${layer_names[_idx]}`,
                'minzoom': PARCELS_ORIGINAL_ZOOM_LEVELS[layer_names[_idx]],
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
            }, `${layer_names[_idx]}-highlighted`);
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
export const searchParcel = (lngLat: maplibregl.LngLat, propertyId: number, callback: (parcel: ParcelInterface) => void) => {
    axios.get(SEARCH_PARCEL_URL + `?lat=${lngLat.lat}&lng=${lngLat.lng}&property_id=${propertyId}`).then((response) => {
        if (response.data) {
            callback(response.data as ParcelInterface)
        } else {
            callback(null)
        }
    }).catch((error) => {
        if (error.response && error.response.status === 404) {
            // perhaps there is other way to stop axios printing 404 to log?
            console.clear()
        }
        callback(null)
    })
}

/**
 * Search property by coordinate
 * Note: LngLat is in srid 4326
 * @param lngLat 
 * @param callback 
 */
export const searchProperty = (lngLat: maplibregl.LngLat, callback: (parcel: PropertyInterface) => void) => {
    axios.get(SEARCH_PROPERTY_URL + `?lat=${lngLat.lat}&lng=${lngLat.lng}`).then((response) => {
        if (response.data) {
            callback(response.data as PropertyInterface)
        } else {
            callback(null)
        }
    }).catch((error) => {
        if (error.response && error.response.status === 404) {
            // perhaps there is other way to stop axios printing 404 to log?
            console.clear()
        }
        callback(null)
    })
}
