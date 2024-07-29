import React from 'react';
import ReactDOM from "react-dom/client";
import maplibregl, { IControl } from 'maplibre-gl';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import html2canvas from "html2canvas";
import { MapTheme, PopulationCountLegend } from "../../../models/Map";
import './legends.scss';


interface LegendPlaceholderInterface {
  species: string;
  year: number;
  data: PopulationCountLegend[];
}


function LegendPlaceholder(props: LegendPlaceholderInterface) {
    return (
      <div className='legend-placeholder'>
        <div className='legend-header'>
          {props.species} population ({props.year})
        </div>
        {props.data.map((item: PopulationCountLegend, index: number) => {
          return (
            <div className='legend-item' key={index}>
              <Grid container flexDirection={'row'} alignItems={'center'}>
                <Grid item className='legend-color'>
                  <Box className='color' sx={{backgroundColor: `${item.color}`}}></Box>
                </Grid>
                <Grid item>
                  {`${item.minLabel} - ${item.maxLabel}`}
                </Grid>
              </Grid>
            </div>
          )
        })}
      </div>
    )
}
  
export default class LegendControl<IControl> {
    _map: maplibregl.Map;
    _container: HTMLElement;
    _divRoot: any;
    _currentZoom: number;
    _year: number;
    _species: string;
    _data: PopulationCountLegend[];
  
    constructor() {
    }

    _initDom() {
      this._container = document.createElement('div');
      
      this._container.className = 'maplibregl-ctrl maplibregl-ctrl-group mapboxgl-ctrl mapboxgl-ctrl-group';
      this._divRoot = ReactDOM.createRoot(this._container)
    }
  
    onAdd(map: maplibregl.Map){
      this._map = map;
      this._currentZoom = -1;
      this._initDom();
      return this._container;
    }
  
    onRemove() {
        this._container.parentNode.removeChild(this._container)
        this._map = undefined
    }

    onUpdateLegends(zoom: number, species: string, year: number, data: PopulationCountLegend[]) {
      this._currentZoom = zoom;
      this._year = year;
      this._data = data;
      this._species = species;
      if (data.length === 0) {
        this.onClearLegends();
      } else {
        this._divRoot.render(<LegendPlaceholder species={species} data={data} year={year}/>);
      }
    }

    onClearLegends() {
      this._currentZoom = -1;
      this._year = -1;
      this._data = [];
      this._species = "";
      this._divRoot.render(<div></div>);
    }

    getContentAsCanvas() {
      if (this._currentZoom === -1) {
        return new Promise((resolve) => {
          resolve(null);
        });
      }
      return html2canvas(this._container, {
        backgroundColor: '#fff',
        scale: 1
      });
    }

    getCurrentZoom() {
      return this._currentZoom;
    }

    getCurrentYear() {
      return this._year;
    }

    getCurrentData() {
      return this._data;
    }

    getCurrentSpecies() {
      return this._species;
    }

    onThemeChanged(theme: MapTheme) {
      if (theme === MapTheme.Dark) {
        this._container.className = 'maplibregl-ctrl maplibregl-ctrl-group mapboxgl-ctrl mapboxgl-ctrl-group legend-root-dark';
      } else {
        this._container.className = 'maplibregl-ctrl maplibregl-ctrl-group mapboxgl-ctrl mapboxgl-ctrl-group';
      }
    }
}
  