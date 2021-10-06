import PropTypes from 'prop-types';
import React from 'react';
// material
import { Box } from '@material-ui/core';

// ----------------------------------------------------------------------

Logo.propTypes = {
  sx: PropTypes.object
};

export default function Logo({ sx }) {
  return <Box component="img" src="/static/engineering.png" sx={{ height: 40, ...sx }} />;
}
