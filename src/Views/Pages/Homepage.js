import React from "react";
import "./Homepage.css";
import { Link } from "react-router-dom";
import { HashLink } from "react-router-hash-link";
import Navbar from "../../Components/Navbar";
// css from StyleSheet.css - bg color change garnu pare change from there
function Homepage() {
  const token = localStorage.getItem("authToken");
  return (
    <body data-bs-spy="scroll" data-bs-target="#navbarExample">
      {/* <!-- Navigation --> */}
      <Navbar />

      {/* <!-- Header --> */}
      <header id="header" class="header">
        <div class="container">
          <div class="row">
            <div class="col-lg-6">
              <div class="text-container">
                <h1 class="h1-large">
                  Business Analytics Tool for Businesses that care!
                </h1>
                <p class="p-large">
                  Find out the public sentiment about a product or brand today.
                </p>
                {token == null && (
                  <Link to="/register" class="btn-solid-lg">
                    Sign up for free
                  </Link>
                )}
                {token !== null && (
                  <HashLink smooth to="#features" class="btn-solid-lg">
                    Learn More!
                  </HashLink>
                )}
              </div>
            </div>
            <div class="col-lg-6">
              <div class="image-container">
                <img
                  marginLeft='100px'
                  class="img-fluid"
                  src="../assets/img/header-illustration.svg"
                  alt="alternative"
                />
              </div>
            </div>
          </div>
        </div>
      </header>
      {/* <!-- Features --> */}
      <div id="features" class="cards-1">
        <div class="container">
          <div class="row">
            <div class="col-lg-12">
              <h2 class="h2-heading">
                Sentiment Analysis of Product Reviews is packed with{" "}<br/>
                <span>awesome features</span>
              </h2>
            </div>
          </div>
          <div class="row">
            <div class="col-lg-12">
              <div class="card">
                <div class="card-icon">
                  <span class="fas fa-headphones-alt"></span>
                </div>
                <div class="card-body">
                  <h4 class="card-title">Customer Sentiments</h4>
                  <p>Analyze customer's opinion on various latest products.</p>
                </div>
              </div>
              <div class="card">
                <div class="card-icon green">
                  <span class="far fa-clipboard"></span>
                </div>
                <div class="card-body">
                  <h4 class="card-title">Sales Tracking</h4>
                  <p>Track sales of a Product based on public likings.</p>
                </div>
              </div>
              <div class="card">
                <div class="card-icon blue">
                  <span class="far fa-comments"></span>
                </div>
                <div class="card-body">
                  <h4 class="card-title">Reporting Tool</h4>
                  <p>Download your analysis report for a product.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* <!-- Details 1 --> */}
      <div id="details" class="basic-1 bg-gray">
        <div class="container">
          <div class="row">
            <div class="col-lg-6 col-xl-5">
              <div class="text-container">
                <h2>
                  Manage your customer’s expectations and get them to trust you
                </h2>
                <p>
                  Building trust is an ongoing process that requires consistency,
                   open communication, and a customer-centric approach. By effectively
                    managing customer expectations and demonstrating your commitment to
                     their satisfaction, you can earn their trust and cultivate strong 
                     and loyal customer relationships.
                </p>
              </div>
            </div>
            <div class="col-lg-6 col-xl-7">
              <div class="image-container">
                <img
                  class="img-fluid"
                  src="../assets/img/details-1.svg"
                  alt="alternative"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* <!-- Invitation --> */}
      {/* <div class="basic-3">
        <div class="container">
          <div class="row">
            <div class="col-lg-12">
              <h4>
                Ioniq will change the way you think about CRM solutions due to
                it’s advanced tools and integrated functionalities
              </h4>
              <Link to="/register" class="btn-outline-lg page-scroll">
                Sign up for free
              </Link>
            </div>
          </div>
        </div>
      </div> */}
      {/* <!-- Pricing --> */}
      {/* <div id="pricing" class="cards-2 bg-gray">
        <div class="container">
          <div class="row">
            <div class="col-lg-12">
              <h2 class="h2-heading">Free forever tier and 2 pro plans</h2>
            </div>
          </div>
          <div class="row">
            <div class="col-lg-12">
              <div class="card">
                <div class="card-body">
                  <div class="card-title">
                    <img
                      class="decoration-lines"
                      src="../assets/img/decoration-lines.svg"
                      alt="alternative"
                    />
                    <span>Free tier</span>
                    <img
                      class="decoration-lines flipped"
                      src="../assets/img/decoration-lines.svg"
                      alt="alternative"
                    />
                  </div>
                  <ul class="list-unstyled li-space-lg">
                    <li>Fusce pulvinar eu mi acm</li>
                    <li>Curabitur consequat nisl bro</li>
                    <li>Reget facilisis molestie</li>
                    <li>Vivamus vitae sem in tortor</li>
                    <li>Pharetra vehicula ornares</li>
                    <li>Vivamus dignissim sit amet</li>
                    <li>Ut convallis aliquama set</li>
                  </ul>
                  <div class="price">Free</div>
                  <a href="sign-up.html" class="btn-solid-reg">
                    Sign up
                  </a>
                </div>
              </div>
              <div class="card">
                <div class="card-body">
                  <div class="card-title">
                    <img
                      class="decoration-lines"
                      src="../assets/img/decoration-lines.svg"
                      alt="alternative"
                    />
                    <span>Advanced</span>
                    <img
                      class="decoration-lines flipped"
                      src="../assets/img/decoration-lines.svg"
                      alt="alternative"
                    />
                  </div>
                  <ul class="list-unstyled li-space-lg">
                    <li>Nunc commodo magna quis</li>
                    <li>Lacus fermentum tincidunt</li>
                    <li>Nullam lobortis porta diam</li>
                    <li>Announcing of invita mro</li>
                    <li>Dictum metus placerat luctus</li>
                    <li>Sed laoreet blandit mollis</li>
                    <li>Mauris non luctus est</li>
                  </ul>
                  <div class="price">
                    $19<span>/month</span>
                  </div>
                  <a href="sign-up.html" class="btn-solid-reg">
                    Sign up
                  </a>
                </div>
              </div>
              <div class="card">
                <div class="card-body">
                  <div class="card-title">
                    <img
                      class="decoration-lines"
                      src="../assets/img/decoration-lines.svg"
                      alt="alternative"
                    />
                    <span>Professional</span>
                    <img
                      class="decoration-lines flipped"
                      src="../assets/img/decoration-lines.svg"
                      alt="alternative"
                    />
                  </div>
                  <ul class="list-unstyled li-space-lg">
                    <li>Quisque rutrum mattis</li>
                    <li>Quisque tristique cursus lacus</li>
                    <li>Interdum sollicitudin maec</li>
                    <li>Quam posuerei pellentesque</li>
                    <li>Est neco gravida turpis integer</li>
                    <li>Mollis felis. Integer id quam</li>
                    <li>Id tellus hendrerit lacinia</li>
                  </ul>
                  <div class="price">
                    $29<span>/month</span>
                  </div>
                  <a href="sign-up.html" class="btn-solid-reg">
                    Sign up
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div> */}
      {/* <!-- Footer --> */}
      <div class="footer">
        <div class="container">
          <div class="row">
            <div class="col-lg-12">
              <div class="footer-col first">
                <h6>About </h6>
                <p class="p-small">
                 Sentiment Analytsis tells you what the public thinks about about
                  the latest products.{" "}
                </p>
              </div>
              <div class="footer-col second"></div>
              <div class="footer-col third">
                <span class="fa-stack">
                  <a href="#your-link">
                    <i class="fas fa-circle fa-stack-2x"></i>
                    <i class="fab fa-facebook-f fa-stack-1x"></i>
                  </a>
                </span>
                <span class="fa-stack">
                  <a href="#your-link">
                    <i class="fas fa-circle fa-stack-2x"></i>
                    <i class="fab fa-twitter fa-stack-1x"></i>
                  </a>
                </span>
                <span class="fa-stack">
                  <a href="#your-link">
                    <i class="fas fa-circle fa-stack-2x"></i>
                    <i class="fab fa-pinterest-p fa-stack-1x"></i>
                  </a>
                </span>
                <span class="fa-stack">
                  <a href="#your-link">
                    <i class="fas fa-circle fa-stack-2x"></i>
                    <i class="fab fa-instagram fa-stack-1x"></i>
                  </a>
                </span>
                <p class="p-small">
                  For further queries please contact us at:{" "}
                  <a href="mailto:contact@site.com">
                    <strong>safalstha818@site.com</strong>
                  </a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* <!-- Copyright --> */}
      <div class="copyright" id="contact">
        <div class="container">
          <div class="row">
            <div class="col-lg-6">
              <p class="p-small" style={{marginLeft:'-250px'}}>
                Copyright © <a href="#your-link">Sentiment Analysis</a>
              </p>
            
            </div>

            <div class="col-lg-6">
             
              <p class="p-small" style={{marginLeft:'250px'}}>
                Designed And Developed By <a href="#your-link">Safal Shrestha</a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </body>
  );
}

export default Homepage;
