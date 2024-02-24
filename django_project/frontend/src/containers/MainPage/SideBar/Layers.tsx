import React, { useEffect, useState } from 'react';
import axios from "axios";
import Box from "@mui/material/Box";
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemIcon from '@mui/material/ListItemIcon';
import Checkbox from '@mui/material/Checkbox';
import Collapse from '@mui/material/Collapse';
import IconButton from '@mui/material/IconButton';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import Tooltip from '@mui/material/Tooltip';
import ContextLayerInterface, { ContextLayerLegendInterface } from '../../../models/ContextLayer';
import {RootState} from '../../../app/store';
import { useAppSelector, useAppDispatch } from '../../../app/hooks';
import { setContextLayers, toggleLayer, toggleExpandedLayer } from '../../../reducers/LayerFilter';
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
                // disable NGI Aerial Imagery by default
                if (layer.name === 'NGI Aerial Imagery') {
                    layer.isSelected = false
                }
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
                        <div key={layer.id}>
                            <ListItem
                                key={layer.id}
                            >
                                <ListItemIcon>
                                    <Checkbox
                                        edge="start"
                                        disabled={loading || !isMapReady}
                                        checked={layer.isSelected}
                                        tabIndex={-1}
                                        disableRipple
                                        inputProps={{ 'aria-labelledby': labelId }}
                                        onClick={(event) => dispatch(toggleLayer(layer.id)) }
                                    />
                                </ListItemIcon>
                                <Tooltip title={layer.description ? layer.description : layer.name}>
                                    <ListItemText id={labelId} primary={layer.name} className='LayerName' onClick={(event) => dispatch(toggleLayer(layer.id))} />
                                </Tooltip>
                                { layer.legends.length && layer.isExpanded ?  <IconButton onClick={(event) => dispatch(toggleExpandedLayer(layer.id))}><ExpandLess /></IconButton> : null }
                                { layer.legends.length && !layer.isExpanded ? <IconButton onClick={(event) => dispatch(toggleExpandedLayer(layer.id))}><ExpandMore /></IconButton> : null }
                            </ListItem>
                            <Collapse in={layer.isExpanded} timeout="auto" unmountOnExit>
                                <List component="div" disablePadding>
                                    {layer.legends.map((legend: ContextLayerLegendInterface) => {
                                        return (
                                            <ListItem key={legend.name}>
                                                <ListItemIcon>
                                                    <Box className='LegendIcon' sx={{ backgroundColor: legend.colour}} />
                                                </ListItemIcon>
                                                <ListItemText primary={legend.name} />
                                            </ListItem>
                                        )
                                    })}
                                </List>
                            </Collapse>
                        </div>
                    )
                })
            }
            </List>
        </Box>
    )

}


export default Layers;
