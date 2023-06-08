import { configureStore, ThunkAction, Action } from '@reduxjs/toolkit';
import LayerFilterReducer from '../reducers/LayerFilter';
import MapStatusReducer from '../reducers/MapStatus';

export const store = configureStore({
    reducer: {
      layerFilter: LayerFilterReducer,
      mapStatus: MapStatusReducer
    },
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
