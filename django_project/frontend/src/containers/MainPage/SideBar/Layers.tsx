import React, { useState } from 'react';
import Box from "@mui/material/Box";
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import ContextLayerInterface from '../../../models/ContextLayer';
import './index.scss';

function Layers() {
    const [selectedLayers, setSelectedLayers] = useState<number[]>([])
    const [availableLayers, setAvailableLayers] = useState<ContextLayerInterface[]>([
        {
            id: 1,
            name: 'Roads'
        },
        {
            id: 2,
            name: 'Rivers'
        },
        {
            id: 3,
            name: 'Properties'
        },
        {
            id: 4,
            name: 'Protected Areas'
        }
    ])

    const handleListItemClick = (
        event: React.MouseEvent<HTMLDivElement, MouseEvent>,
        layerId: number,
      ) => {
        let _selected = [...selectedLayers]
        let _idx = _selected.indexOf(layerId)
        if (_idx !== -1) {
            _selected.splice(_idx, 1)
            setSelectedLayers(_selected)
        } else {
            setSelectedLayers([..._selected, layerId])
        }
    }

    return (
        <Box className={'Layers'}>
            <List component="nav" aria-label="layers">
            {
                availableLayers.map((layer: ContextLayerInterface) => {
                    return (
                        <ListItemButton
                            key={layer.id}
                            selected={selectedLayers.indexOf(layer.id) !== -1}
                            onClick={(event) => handleListItemClick(event, layer.id)}
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
