import React from 'react';
import ReactDOM from "react-dom/client";
import maplibregl, { IControl } from 'maplibre-gl';

function LegendPlaceholder(props: any) {
    return (
      <div className='legend-placeholder'>
        <div className='legend-header'>
          LEGEND
        </div>
        <div className='legend-item'>
          Properties
        </div>
        <div className='legend-item'>
          Rivers
        </div>
        <div className='legend-item'>
          Roads
        </div>
        <div className='legend-item'>
          Places
        </div>
      </div>
    )
}
  
export default class LegendControl<IControl> {
    _map: maplibregl.Map;
    _container: HTMLElement;
  
    constructor() {
  
    }
  
    onAdd(map: maplibregl.Map){
      this._map = map;
      this._container = document.createElement('div');
      this._container.className = 'maplibregl-ctrl maplibregl-ctrl-group mapboxgl-ctrl mapboxgl-ctrl-group';
      const divRoot = ReactDOM.createRoot(this._container)
      divRoot.render(<LegendPlaceholder />);
      return this._container;
    }
  
    onRemove() {
        this._container.parentNode.removeChild(this._container)
        this._map = undefined
    }
  
}
  
  