import { configureStore, ThunkAction, Action } from '@reduxjs/toolkit';
import LayerFilterReducer from '../reducers/LayerFilter';
import MapStateReducer from '../reducers/MapState';

export const store = configureStore({
    reducer: {
      layerFilter: LayerFilterReducer,
      mapState: MapStateReducer
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
