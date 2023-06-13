import React, { useEffect, useState } from 'react';
import axios from "axios";
import Box from "@mui/material/Box";
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import ListItemIcon from '@mui/material/ListItemIcon';
import Checkbox from '@mui/material/Checkbox';
import ContextLayerInterface from '../../../models/ContextLayer';
import {RootState} from '../../../app/store';
import { useAppSelector, useAppDispatch } from '../../../app/hooks';
import { setContextLayers, toggleLayer } from '../../../reducers/LayerFilter';
import Loading from '../../../components/Loading';
import './index.scss';

const FETCH_AVAILABLE_CONTEXT_LAYERS = '/api/map/search/context_layer/list/'

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
    }, [])

    return (
        <Box className={'Layers'}>
            <List component="nav" aria-label="layers">
            { loading ? <Loading /> :
                contextLayers.map((layer: ContextLayerInterface) => {
                    const labelId = `checkbox-list-label-${layer.id}`;
                    return (
                        <ListItemButton
                            key={layer.id}
                            disabled={loading || !isMapReady}
                            onClick={(event) => dispatch(toggleLayer(layer.id))}
                        >
                            <ListItemIcon>
                                <Checkbox
                                edge="start"
                                checked={layer.isSelected}
                                tabIndex={-1}
                                disableRipple
                                inputProps={{ 'aria-labelledby': labelId }}
                                />
                            </ListItemIcon>
                            <ListItemText id={labelId} primary={layer.name} />
                        </ListItemButton>
                    )
                })
            }
            </List>
        </Box>
    )

}


export default Layers;
