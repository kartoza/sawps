import React, { useRef, useEffect } from 'react';
import maplibregl, {} from 'maplibre-gl';
import PropertyInterface from '../../models/Property';


const MAP_STYLE_URL = window.location.origin + '/api/map/styles/'

interface MapPreviewInterface {
    propertyItem: PropertyInterface;
}

export default function MapPreview(props: MapPreviewInterface) {
    const { propertyItem } = props
    const mapContainer = useRef(null);
    const map = useRef(null);
    
    useEffect(() => {
        if (propertyItem === null) return
        if (map.current === null) {
            let _center = new maplibregl.LngLat(25.03362151950985, -29.12771414496658)
            if (propertyItem.centroid) {
                _center = new maplibregl.LngLat(propertyItem.centroid[0], propertyItem.centroid[1])
            }
            if (propertyItem.size <= 200 && propertyItem.bbox) {
                let _bbox = propertyItem.bbox
                map.current = new maplibregl.Map({
                    container: mapContainer.current,
                    style: `${MAP_STYLE_URL}`,
                    minZoom: 12,
                    center: _center,
                    bounds: [[_bbox[0], _bbox[1]], [_bbox[2], _bbox[3]]]
                })
            } else {
                map.current = new maplibregl.Map({
                    container: mapContainer.current,
                    style: `${MAP_STYLE_URL}`,
                    minZoom: 12,
                    center: _center
                })
            }
        }
    }, [propertyItem])


    return (
        <div className="map-wrap">
          <div ref={mapContainer} className="map" />
        </div>
    )
}
