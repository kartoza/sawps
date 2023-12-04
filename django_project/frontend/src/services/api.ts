import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";

const baseQuery = fetchBaseQuery({
    baseUrl: '/'  // Base URL for all API requests
})

export interface UserInfo {
    user_permissions: string[],
    user_roles: string[],
    current_organisation_id: number,
    current_organisation: string
}

export interface Property {
  id: number
  short_code: string
  name: string
  owner: string
  owner_email: string
  property_type: string
  property_type_id: number
  province: string
  province_id: number
  open: string
  open_id: number
  size: number
  organisation: string
  organisation_id: number
}

export interface Organisation {
  id: number
  name: string
  national: boolean
  use_of_data_by_sanbi_only: boolean
  hosting_through_sanbi_platforms: boolean
  allowing_sanbi_to_expose_data: boolean
  data_use_permission: number
  province: number
}

export interface Species {
  id: number
  scientific_name: string
  common_name_verbatim: string
}

export interface TaxonDetail {
  id: number
  species_name: string
  graph_icon: any
  topper_icon: any
  total_population: number
  total_area: number
  colour: string
  model_updated_on: Date
}

export interface Activity {
  id: number
  name: string
  recruitment: boolean
  colour: string
  width: number
  export_fields: string[]
}

export interface PropertyType {
  id: number
  name: string
  colour: string
}

export interface Province {
  id: number
  name: string
}

// Create an API slice using RTK Query's createApi.
// This defines a set of endpoints related to user operations.
export const userApi = createApi({
    baseQuery: baseQuery,
    tagTypes: ['User', 'Organisation', 'Activity', 'Property', 'Species', 'Taxon', 'PropertyType', 'Province'],
    endpoints: (build) => ({
        getUserInfo: build.query<UserInfo, void>({
            query: () => 'api/user-info/',
            transformResponse: (response: UserInfo) => {
                return response;
            },
            providesTags: ['User']
        }),
          getOrganisation: build.query<Organisation[], void>({
            query: () => 'api/organisation/',
            transformResponse: (response: Organisation[]) => {
                return response;
            },
            providesTags: ['Organisation']
        }),
        getActivity: build.query<Activity[], void>({
            query: () => 'api/activity-type/',
            transformResponse: (response: Activity[]) => {
                return response;
            },
            providesTags: ['Activity']
        }),
        getActivityAsObj: build.query<Activity[], void>({
            query: () => 'api/activity-type/',
            transformResponse: (response: Activity[]) => {
                return response;
            },
            providesTags: ['Activity']
        }),
        getProperty: build.query<Property[], string>({
            query: (organisationIds: string) => `api/property/list/?organisation=${organisationIds}`,
            transformResponse: (response: Property[]) => {
                return response;
            },
            providesTags: ['Property']
        }),
        getSpecies: build.query<Species[], string>({
            query: (organisationIds: string) => `species/?organisation=${organisationIds}`,
            transformResponse: (response: Species[]) => {
                return response;
            },
            providesTags: ['Species']
        }),
        getTaxonDetail: build.query<TaxonDetail, string>({
            query: (species_name: string) => `api/species/trend-page/?species=${species_name}`,
            transformResponse: (response: TaxonDetail) => {
                return response;
            },
            providesTags: ['Taxon']
        }),
        getPropertyType: build.query<PropertyType[], void>({
            query: () => 'api/property/types/',
            transformResponse: (response: PropertyType[]) => {
                return response;
            },
            providesTags: ['PropertyType']
        }),
        getProvince: build.query<Province[], void>({
            query: () => 'api/province/',
            transformResponse: (response: Province[]) => {
                return response;
            },
            providesTags: ['Province']
        }),
    })
})


export const {
    useGetUserInfoQuery,
    useGetOrganisationQuery,
    useGetActivityQuery,
    useGetActivityAsObjQuery,
    useGetPropertyQuery,
    useGetSpeciesQuery,
    useGetTaxonDetailQuery,
    useGetPropertyTypeQuery,
    useGetProvinceQuery
} = userApi


