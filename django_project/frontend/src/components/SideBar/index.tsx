import React from 'react';
import './index.scss';

import {
    Autocomplete,
    Box,
    Checkbox,
    Divider,
    FormControlLabel,
    Paper,
    TextField,
    Typography
} from '@mui/material';


interface SideBarProps {
    items?: string[]
}

export default function SideBar(props: SideBarProps) {
    return (
        <div className='SideBar'>

        </div>
    )
}

interface AutoCompleteCheckboxProps {
  options: any[],
  selectedOption: any[],
  singleTerm: string,
  pluralTerms: string,
  selectAllFlag: boolean,
  setSelectAll(value: boolean): void,
  setSelectedOption(values: any[]): void,
  setSelectedOption(values: any[]): void,
}


export function AutoCompleteCheckbox(props: AutoCompleteCheckboxProps) {
  const {
    options,
    selectedOption,
    singleTerm,
    pluralTerms,
    selectAllFlag,
    setSelectAll,
    setSelectedOption
  } = props

  return (
      <Autocomplete
          multiple
          options={options}
          fullWidth
          disableCloseOnSelect
          freeSolo={false}
          value={options.filter((option) => selectedOption.includes(option.id))}
          getOptionLabel={(option) => option.name}
          renderOption={(props, option, { selected }) => (
            <li {...props}>
                <FormControlLabel
                    style={{color: 'black'}}
                    label={option.name}
                    control={
                      <Checkbox
                        checked={selectedOption.includes(option.id)}
                        style={{color: 'black'}}
                      />
                    }
                  />
            </li>
          )}
          renderTags={(value, getTagProps) => {
            const numTags = value.length;
            const field = numTags > 1 ? singleTerm : pluralTerms

            return <Typography
              className={'autoComplete-Tags'}
              variant="body2">
                {numTags} {field} selected
            </Typography>;
          }}
          onChange={(_e, value, reason) => {
            if (reason === "clear")
              setSelectAll(false);
            else if (
              reason === "selectOption" && value.length === options.length
            )
              setSelectAll(true);
            else if (
              reason === "removeOption" && value.length === 0
            ) {
                setSelectAll(false);
            }
            else if (
              reason === "removeOption" || reason === "selectOption"
            ) {
                const valueIds = value.map(val => val.id)
                setSelectedOption(valueIds);
            }
          }}
          renderInput={(params) => (
            <TextField {...params}/>
          )}
          PaperComponent={(paperProps) => {
            const { children, ...restPaperProps } = paperProps;
            return (
              <Paper {...restPaperProps}>
                <Box
                  onMouseDown={(e) => e.preventDefault()} // prevent blur
                  pl={1.5}
                  py={0.5}
                >
                  <FormControlLabel
                    onClick={(e) => {
                      e.preventDefault(); // prevent blur
                      setSelectAll(!selectAllFlag);
                    }}
                    style={{color: 'black'}}
                    label="Select All"
                    control={
                      <Checkbox checked={selectAllFlag} style={{color: 'black'}}/>
                    }
                  />
                </Box>
                <Divider />
                {children}
              </Paper>
            );
          }}
        />
    )
}