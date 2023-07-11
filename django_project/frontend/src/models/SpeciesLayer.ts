export default interface SpeciesLayer {
    id: number
    scientific_name: string,
    common_name_varbatim: string,
    colour_variant: boolean,
    infraspecific_epithet: string | null,
    taxon_rank: number,
    parent: string | null, 
    isSelected:boolean,
}