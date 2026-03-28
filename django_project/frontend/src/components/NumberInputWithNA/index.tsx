import React, { useState, useEffect, ChangeEvent } from 'react';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import { SvgIconProps } from '@mui/material/SvgIcon';

interface NumberInputWithNAProps {
  initialValue?: number | null;
  onValueChange?: (value: number) => void;
  label?: string;
  icon?: React.ReactElement<SvgIconProps>;
  id?: string;
  helperText?: string;
  onValidationError?: () => void;
}

const NumberInputWithNA: React.FC<NumberInputWithNAProps> = ({
  initialValue = null,
  onValueChange,
  label,
  icon,
  id,
  helperText = " ",
  onValidationError
}) => {
  const [value, setValue] = useState<string>(initialValue === null ? 'NA' : String(initialValue));
  const [validValue, setValidValue] = useState<string>(value);
  const [error, setError] = useState<boolean>(false);

  useEffect(() => {
    const newValue = initialValue === null ? 'NA' : String(initialValue);
    setValue(newValue);
    setValidValue(newValue);
    setError(false);
  }, [initialValue]);

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const inputValue = event.target.value;
    const sanitizedValue = inputValue.replace(/^0+(?!\.|$)/, '');
    
    // Perform full input validation when necessary
    if (/^(\d*|NA)$/i.test(sanitizedValue)) {
        setValidValue(sanitizedValue);
        setValue(sanitizedValue);
        setError(false);
        // Notify parent component of the change
        if (onValueChange) {
            if (sanitizedValue.toLowerCase().startsWith('na')) {
                onValueChange(null);
            } else {
                onValueChange(parseInt(sanitizedValue));
            }
        }
    } else {
        setValue(inputValue);
        setError(true);
        if (onValidationError) {
            onValidationError();
        }
    }
  };

  return (
    <TextField
      id={id}
      label={label}
      value={value}
      onChange={handleChange}
      placeholder="Enter a number or 'NA'"
      variant="standard"
      fullWidth
      InputProps={{
        startAdornment: icon ? (
          <InputAdornment position="start">
            {icon}
          </InputAdornment>
        ) : null,
        title: "Please enter a valid number or 'NA'"
      }}
      inputProps={{
        pattern: '(\d*|NA)',
      }}
      helperText={error ? 'Please enter a valid number or NA' : helperText}
      error={error}
    />
  );
}

export default NumberInputWithNA;
