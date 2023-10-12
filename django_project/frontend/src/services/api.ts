import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";

const baseQuery = fetchBaseQuery({
    baseUrl: '/'  // Base URL for all API requests
})

export interface UserInfo {
    user_roles: string[],
    current_organisation_id: number,
    current_organisation: string
}

// Create an API slice using RTK Query's createApi.
// This defines a set of endpoints related to user operations.
export const userApi = createApi({
    baseQuery: baseQuery,
    tagTypes: ['User'],
    endpoints: (build) => ({
        getUserInfo: build.query<UserInfo, void>({
            query: () => 'api/user-info/',
            transformResponse: (response: UserInfo) => {
                return response;
            },
            providesTags: ['User']
        }),
    })
})

export const {
    useGetUserInfoQuery
} = userApi

