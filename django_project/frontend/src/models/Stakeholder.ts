
export interface OrganisationInterface {
    id: number,
    name: string
}

export enum UserRole {
    SUPERUSER = 'Super user',
    ADMIN = 'Admin',
    DECISION_MAKER = 'Decision maker',
    DATA_CONTRIBUTOR = 'Data contributor'
}
