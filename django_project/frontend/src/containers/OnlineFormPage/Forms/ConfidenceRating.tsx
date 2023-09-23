import React from 'react';
import {
  Modal,
  Typography,
  Slider,
  Paper,
  Grid,
  Button,
} from '@mui/material';

interface ConfidenceRatingProps {
  open: boolean;
  onClose: () => void;
  onSubmit: () => void;
  currentConfidence: number;
  onConfidenceChange: (newValue: number) => void;
  modalHeight?: string;
}

const ConfidenceRating: React.FC<ConfidenceRatingProps> = ({
  open,
  onClose,
  onSubmit,
  currentConfidence,
  onConfidenceChange,
  modalHeight = 'auto',
}) => {
  const handleSliderChange = (event: Event, newValue: number | number[]) => {
    if (typeof newValue === 'number') {
      onConfidenceChange(newValue);
    }
  };

  const handleValueClick = (value: number) => {
    onConfidenceChange(value);
  };

  const renderValues = () => {
    const values = Array.from({ length: 10 }, (_, index) => index + 1);

    return (
      <Grid container spacing={2} justifyContent="center">
        {values.map((value) => (
          <Grid item key={value}>
            <Paper
              sx={{
                padding: 2,
                textAlign: 'center',
                backgroundColor:
                  value === currentConfidence ? '#f0f0f0' : 'inherit',
                cursor: 'pointer', // Add cursor style
              }}
              onClick={() => handleValueClick(value)}
            >
              {value}
            </Paper>
          </Grid>
        ))}
      </Grid>
    );
  };

  return (
    <Modal open={open} onClose={onSubmit}>
      <Paper
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: '40%',
          height: modalHeight,
          p: 4,
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        <Typography variant="h6" align="center">
          Population Estimate Certainty
        </Typography>
        <Typography variant="body1" align="left" mt={1}>
          How confident are you that this estimate is close to the true population size?
        </Typography>
        <Typography
          variant="body2"
          mt={1}
          textAlign="center"
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
          }}
        >
          {currentConfidence === 1 && 'Least confident'}
          {currentConfidence === 10 && 'Most confident'}
        </Typography>
        <Slider
          value={currentConfidence}
          onChange={handleSliderChange}
          min={1}
          max={10}
          step={1}
        />
        {renderValues()}
        <Button
          variant="contained"
          onClick={onSubmit}
          sx={{ alignSelf: 'flex-end', mt: 2 }}
        >
          Submit
        </Button>
      </Paper>
    </Modal>
  );
};

export default ConfidenceRating;
