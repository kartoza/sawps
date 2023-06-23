import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import './index.scss';

const pages = ['Map'];
const menuItems = [{
  'title': 'Profile',
  'href': '/'
}, {
  'title': 'Account',
  'href': '/',
}, {
  'title': 'Dashboard',
  'href': '/',
}, {
  'title': 'Logout',
  'href': '/accounts/logout'
}];
const isLoggedIn = (window as any).isLoggedIn;

function ResponsiveNavbar() {
  const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(null);
  const [anchorElUser, setAnchorElUser] = React.useState<null | HTMLElement>(null);

  const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = (page: string = "") => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  return (
    <AppBar position="static" className='navbar navbar-dark'>
      <Box sx={{width: '100%'}}>
        <Toolbar disableGutters>
          <Box sx={{ p: 1, display: { xs: 'none', md: 'flex' } }}>
            <a href='/'>
              <img
                src='/static/images/SANBI-logo.jpg'
                alt="Logo"
                style={{
                  height: 'auto',
                  maxWidth: 'calc(100% - 16px)'
                }}
              />
            </a>
          </Box>

          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: 'block', md: 'none' },
              }}
            >
              {pages.map((page) => (
                <MenuItem key={page} onClick={() => window.location.href = `\\${page.toLowerCase()}\\`}>
                  <Typography textAlign="center">{page}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
            {pages.map((page) => (
              <Button
                key={page}
                onClick={() => window.location.href = `\\${page.toLowerCase()}\\`}
                sx={{ my: 2, display: 'block' }}
              >
                {page}
              </Button>
            ))}
          </Box>

          {isLoggedIn ?
            <Box sx={{ flexGrow: 0 }}>
              <Tooltip title="Open settings">
                <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                  <Avatar alt="User" src="/static/images/avatar/2.jpg" />
                </IconButton>
              </Tooltip>
              <Menu
                sx={{ mt: '45px' }}
                id="menu-appbar"
                anchorEl={anchorElUser}
                anchorOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
                keepMounted
                transformOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
                open={Boolean(anchorElUser)}
                onClose={handleCloseUserMenu}
              >
                {menuItems.map((menuItem) => (
                  <MenuItem key={menuItem.title}
                    onClick={() => window.location.href = menuItem.href}>
                    <Typography textAlign="center">{menuItem.title}</Typography>
                  </MenuItem>
                ))}
              </Menu>
            </Box> :
            <Box sx={{ display: 'flex', flexDirection: 'row' }}>
              <Button
                key='sign-in'
                href='/accounts/login'
                sx={{ my: 2, display: 'block' }}
              >
                Log In
              </Button>
              <Button
                key='sign-up'
                href='/accounts/signup'
                sx={{ my: 2, display: 'block', ml: 2 }}
              >
                Sign Up
              </Button>
            </Box>
          }
        </Toolbar>
      </Box>
    </AppBar>
  );
}
export default ResponsiveNavbar;
