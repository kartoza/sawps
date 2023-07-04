import axios from "axios";
import ContextLayerInterface from '../../../models/ContextLayer';
import ParcelInterface from '../../../models/Parcel';
import PropertyInterface from "../../../models/Property";

const SEARCH_PARCEL_URL = '/api/map/search/parcel/'
const SEARCH_PROPERTY_URL = '/api/map/search/property/'
export const MIN_SELECT_PARCEL_ZOOM_LEVEL = 12
export const MIN_SELECT_PROPERTY_ZOOM_LEVEL = 12
const PARCELS_ORIGINAL_ZOOM_LEVELS: any = {
    'erf': 14,
    'holding': 12,
    'farm_portion': 12
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
 * Find context layer from Biodiversity, Ecosystems, Protected Areas
 * @param contextLayers 
 * @returns 
 */
export const findAreaLayers = (contextLayers: ContextLayerInterface[]): string[] => {
    const areaLayers = ['ecosystem type', 'biodiversity areas', 'protected areas']
    let _layers = contextLayers.reduce((acc, element) => {
        if (element.isSelected && areaLayers.includes(element.name.toLowerCase())) {
            acc.push(...element.layer_names)
        }
        return acc;
    }, [])
    return _layers
}

/**
 * Check if context layer is selected
 * @param contextLayers 
 * @returns 
 */
export const isContextLayerSelected = (contextLayers: ContextLayerInterface[], contextLayerName: string): boolean => {
    let _layer = contextLayers.find((element) => element.name.toLowerCase() === contextLayerName)
    if (_layer) {
        return _layer.isSelected
    }
    return false
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
            // console.clear()
        }
        callback(null)
    })
}

const FEATURE_NAME_MAPPING:{ [id: string] : string; } = {
    'ecosystems': 'biome_18',
    'biodiversity': 'sensfeat',
    'protected': 'site_type',
    'erf': 'cname',
    'farm_portion': 'cname',
    'holding': 'cname'
}

const GROUP_NAME_MAPPING:{ [id: string] : string; } = {
    'ecosystems': 'Ecosystem Type',
    'biodiversity': 'Critical Biodiversity Area',
    'protected': 'Site Type',
    'erf': 'Erf Cname',
    'farm_portion': 'Farm Portion Cname',
    'holding': 'Holding Cname'
}

/**
 * Get value from feature based on sourceLayer
 * @param feature GeoJson Object
 * @returns 
 */
const getPropertyOfFeature = (feature: any):[string, string] => {
    let _feature_key = null
    let _feature_map_key = null
    for (let _map_key in FEATURE_NAME_MAPPING) {
        if (feature['sourceLayer'].includes(_map_key)) {
            _feature_map_key = _map_key
            _feature_key = FEATURE_NAME_MAPPING[_map_key]
            break;
        }
    }
    if (_feature_key === null) return [null, null]
    if ('properties' in feature && _feature_key in feature['properties']) {
        return [_feature_map_key, feature['properties'][_feature_key]]
    }
    return [null, null]
}

const concatFeatureValues = (feature_map_key: string, featureValues: string[]): string => {
    if (featureValues.length === 2)
        return `${GROUP_NAME_MAPPING[feature_map_key]}: ${featureValues[0]} and ${featureValues[1]}`
    return `${GROUP_NAME_MAPPING[feature_map_key]}: ${featureValues.join(', ')}`
}

export const getMapPopupDescription = (features: Object[]):string => {
    console.log(features)
    // group by source-layer
    let _groups:{ [id: string] : string[]; } = {}
    for (let i=0; i < features.length; ++i) {
        let _feature:any = features[i]
        let [_feature_map_key, _featureValue] = getPropertyOfFeature(_feature)
        if (_featureValue) {
            if (_feature_map_key in _groups) {
                _groups[_feature_map_key].push(_featureValue)
            } else {
                _groups[_feature_map_key] = [_featureValue]
            }
        }
    }
    let _html_result = ''
    if (Object.keys(_groups).length === 0) return _html_result
    if (Object.keys(_groups).length === 1) {
        let _group = Object.keys(_groups)[0]
        _html_result += concatFeatureValues(_group, _groups[_group])
    } else {
        _html_result += '<ul>'
        for (let _group in _groups) {
            let _featureValues = concatFeatureValues(_group, _groups[_group])
            _html_result += `<li>${_featureValues}</li>`
        }
        _html_result += '</ul>'
    }
    console.log(_html_result)
    return _html_result
}
