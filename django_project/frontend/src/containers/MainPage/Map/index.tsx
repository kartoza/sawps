import React, { useRef, useEffect, useState } from 'react';
import maplibregl from 'maplibre-gl';
import './index.scss';

const MAP_STYLE_URL = window.location.origin + '/api/map/styles/'

export default function Map() {
    const mapContainer = useRef(null);
    const map = useRef(null);

    useEffect(() => {
        if (map.current) return; //stops map from intializing more than once
        map.current = new maplibregl.Map({
          container: mapContainer.current,
          style: `${MAP_STYLE_URL}`
        });
    });

    return (
        <div className="map-wrap">
          <div ref={mapContainer} className="map" />
        </div>
    );
}
