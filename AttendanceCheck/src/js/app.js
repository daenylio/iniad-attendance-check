import $ from 'jquery'
window.$ = window.jQuery = $

import other from './components/other'

$(document).ready(() => {
  [
    other
  ].forEach((component) => component.initialize());
})
