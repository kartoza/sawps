import React, {ReactNode} from "react";
import {Box, Card, Typography} from "@mui/material";
import Loading from "../../../components/Loading";

type ChartCardProps = {
    loading: boolean;
    chartComponent: ReactNode;
    title: string;
    xLabel: string;
};

export const ChartCard: React.FC<ChartCardProps> = ({ loading, chartComponent, title , xLabel}) => {
    return (
        <Card className={'card-chart'}>
            {!loading ? (
                <Box className="white-chart">
                    <Typography>{title}</Typography>
                    {chartComponent}
                    <Typography>{xLabel}</Typography>
                </Box>
            ) : (
                <Loading containerStyle={{ minHeight: 160 }} />
            )}
        </Card>
    );
};
