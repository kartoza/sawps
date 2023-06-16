import { configureStore, ThunkAction, Action } from '@reduxjs/toolkit';
import LayerFilterReducer from '../reducers/LayerFilter';
import MapStateReducer from '../reducers/MapState';
import UploadStateReducer from '../reducers/UploadState';

export const store = configureStore({
    reducer: {
      layerFilter: LayerFilterReducer,
      mapState: MapStateReducer,
      uploadState: UploadStateReducer
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
