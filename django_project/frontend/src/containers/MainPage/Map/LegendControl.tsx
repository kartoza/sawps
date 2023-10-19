import React from 'react';
import ReactDOM from "react-dom/client";
import maplibregl, { IControl } from 'maplibre-gl';

function LegendPlaceholder(props: any) {
    return (
      <div className='legend-placeholder'>
        <div className='legend-header'>
          SPECIES NAME POPULATION
        </div>
        <div className='legend-item'>
          1 - 15
        </div>
        <div className='legend-item'>
          16 - 20
        </div>
        <div className='legend-item'>
          21 - 25
        </div>
        <div className='legend-item'>
          26 - 30
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
  
  