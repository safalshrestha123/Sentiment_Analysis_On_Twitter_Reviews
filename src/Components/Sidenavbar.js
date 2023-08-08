import React, { useContext } from "react";
import { Link, NavLink } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import AuthContext from "../context/AuthContext";

function Sidenavbar() {
  let { logoutUser } = useContext(AuthContext);
  function logoutHandler() {
    // console.log("logout");
    logoutUser();
  }
  return (
    <aside
      className="sidenav navbar navbar-vertical navbar-expand-xs border-0 border-radius-xl my-3 fixed-start ms-3   bg-gradient-dark"
      id="sidenav-main"
    >
      <div className="sidenav-header">
        <i
          className="fas fa-times p-3 cursor-pointer text-white opacity-5 position-absolute end-0 top-0 d-none d-xl-none"
          aria-hidden="true"
          id="iconSidenav"
        ></i>
        <br />
        <Link to="/" className="navbar-brand m-0">
          <img
            // src="../assets/img/logo-ct.png"
            src="../assets/img/logo2.png"
            className="navbar-brand-img h-100"
            alt="main_logo"
          />
          <span className="ms-1 font-weight-bold text-white">
          Sentiment Analysis
          </span>
        </Link>
      </div>
      <hr className="horizontal light mt-0 mb-2" />
      <div
        className="collapse navbar-collapse  w-auto  max-height-vh-100"
        id="sidenav-collapse-main"
      >
        <ul className="navbar-nav">
          <li className="nav-item">
            <NavLink
              to="/dashboard"
              className={({ isActive }) =>
                isActive
                  ? "nav-link text-white active bg-primary"
                  : "nav-link text-white"
              }
            >
              <div className="text-white text-center me-2 d-flex align-items-center justify-content-center">
                <i className="material-icons opacity-10">dashboard</i>
              </div>
              <span className="nav-link-text ms-1">Dashboard</span>
            </NavLink>
          </li>
          {/* <li className="nav-item">
            <Link to="/tables" className="nav-link text-white">
              <div className="text-white text-center me-2 d-flex align-items-center justify-content-center">
                <i className="material-icons opacity-10">table_view</i>
              </div>
              <span className="nav-link-text ms-1">Tables</span>
            </Link>
          </li> */}
          {/* <li className="nav-item">
            <a className="nav-link text-white " href="../pages/calendar.html">
              <div className="text-white text-center me-2 d-flex align-items-center justify-content-center">
                <i className="material-icons opacity-10">calendar_today</i>
              </div>
              <span className="nav-link-text ms-1">Calendar</span>
            </a>
          </li> */}
          {/* <li className="nav-item">
            <a
              className="nav-link text-white "
              href="../pages/notifications.html"
            >
              <div className="text-white text-center me-2 d-flex align-items-center justify-content-center">
                <i className="material-icons opacity-10">notifications</i>
              </div>
              <span className="nav-link-text ms-1">Notifications</span>
            </a>
          </li> */}
          <li className="nav-item mt-3">
            <h6 className="ps-4 ms-2 text-uppercase text-xs text-white font-weight-bolder opacity-8">
              Account pages
            </h6>
          </li>
          <li className="nav-item">
            <NavLink
              to="/profile"
              className={({ isActive }) =>
                isActive
                  ? "nav-link text-white active bg-primary"
                  : "nav-link text-white"
              }
            >
              <div className="text-white text-center me-2 d-flex align-items-center justify-content-center">
                <i className="material-icons opacity-10">person</i>
              </div>
              <span className="nav-link-text ms-1">Profile</span>
            </NavLink>
          </li>
          <li
            className="nav-item"
            style={{ color: "pointer" }}
            onClick={logoutHandler}
          >
            <div className="nav-link text-white" style={{ cursor: "pointer" }}>
              <div className="text-white text-center me-2 d-flex align-items-center justify-content-center">
                <i className="material-icons opacity-10">logout</i>
              </div>
              <div>
                <span className="nav-link-text ms-1">Logout</span>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </aside>
  );
}

export default Sidenavbar;
