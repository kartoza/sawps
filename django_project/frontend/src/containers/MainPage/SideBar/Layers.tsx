import React, { useEffect, useState } from 'react';
import axios from "axios";
import Box from "@mui/material/Box";
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import ContextLayerInterface from '../../../models/ContextLayer';
import {RootState} from '../../../app/store';
import { useAppSelector, useAppDispatch } from '../../../app/hooks';
import { setContextLayers, toggleLayer } from '../../../reducers/LayerFilter';
import Loading from '../../../components/Loading';
import './index.scss';

const FETCH_AVAILABLE_CONTEXT_LAYERS = '/api/map/context_layer/list/'

function Layers() {
    const dispatch = useAppDispatch()
    const contextLayers = useAppSelector((state: RootState) => state.layerFilter.contextLayers)
    const isMapReady = useAppSelector((state: RootState) => state.mapState.isMapReady)
    const [loading, setLoading] = useState(false)

    const fetchContextLayers = () => {
        setLoading(true)
        axios.get(FETCH_AVAILABLE_CONTEXT_LAYERS).then((response) => {
            setLoading(false)
            if (response.data) {
              let _layers = response.data as ContextLayerInterface[]
              _layers = _layers.map((layer) => {
                layer.isSelected = true
                return layer
              })
              dispatch(setContextLayers(_layers))
            }
        })
    }

    useEffect(() => {
        if (contextLayers.length === 0) {
            fetchContextLayers()
        }
    }, [contextLayers])

    return (
        <Box className={'Layers'}>
            <List component="nav" aria-label="layers">
            { loading ? <Loading /> :
                contextLayers.map((layer: ContextLayerInterface) => {
                    return (
                        <ListItemButton
                            key={layer.id}
                            selected={layer.isSelected}
                            disabled={loading || !isMapReady}
                            onClick={(event) => dispatch(toggleLayer(layer.id))}
                        >
                            <ListItemText primary={layer.name} />
                        </ListItemButton>
                    )
                })
            }
            </List>
        </Box>
    )

}


export default Layers;
