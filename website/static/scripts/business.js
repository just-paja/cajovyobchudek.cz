const locale = {
  hours: {
    single: 'hodinu',
    low: '%s hodiny',
    high: '%s hodin',
  },
  minutes: {
    single: 'minutu',
    low: '%s minuty',
    high: '%s minut',
  }
}

function getMapStr(map, value) {
  if (value === 1) {
    return map.single
  }
  if (value > 1 && value < 5) {
    return map.low
  }
  return map.high
}

function formatUnits(unit, value) {
  const map = locale[unit]
  const str = getMapStr(map, value)
  return str.replace('%s', Math.round(value))
}

function getFuzzyMinutes (value) {
  if (value <= 4) {
    return 'pár minut'
  }
  if (value <= 9) {
    return 'několik minut'
  }
  if (value < 12) {
    return 'deset minut'
  }
  if (value <= 17) {
    return 'čtvrt hodiny'
  }
  if (value <= 25) {
    return 'dvacet minut'
  }
  if (value <= 35) {
    return 'půl hodiny'
  }
  if (value <= 50) {
    return 'třičtvrtě hodiny'
  }
  return value
}

function getFuzzyStr (duration) {
  if (duration.hours) {
    return formatUnits('hours', duration.hours)
    
  }
  return getFuzzyMinutes(duration.minutes)
}

function getBusinessStatusMessage(closingTime, openingTime) {
  const now = luxon.DateTime.local()
  if (closingTime) {
    let pause = ''
    if (openingTime && openingTime.hasSame(closingTime, 'day')) {
      const diff = openingTime.diff(closingTime, ['hours'])
      pause = ' a pak si dáme pauzu na ' + formatUnits('hours', diff.hours)
    }
    const relative = closingTime.diff(now, ['hours', 'minutes', 'seconds'])
    if (relative.hours > 1 || pause) {
      return 'Dnes máme otevřeno ještě ' + getFuzzyStr(relative.values) + pause + '.'
    }
    return 'Zavíráme za ' + getFuzzyStr(relative.values) + '.'
  } else if (openingTime) {
    return 'Otevřeme ' + openingTime.toLocaleString(luxon.DateTime.DATETIME_SHORT) + '.'
  }
  return 'Zrovna máme zavřeno.'
}

function formatBusinessStatus(el) {
  const closingTime = el.dataset.closingTime
  const openingTime = el.dataset.openingTime
  const message = getBusinessStatusMessage(
    closingTime && luxon.DateTime.fromISO(closingTime), 
    openingTime && luxon.DateTime.fromISO(openingTime)
  )
  el.innerHTML = message
}

function openNewWindow(e) {
  e.preventDefault()
  window.open(e.currentTarget.href)
}

function formatExternalLink(el) {
  el.addEventListener('click', openNewWindow)
}

function formatElement(selector, formatter) {
  const elements = document.querySelectorAll(selector)
  Array.prototype.map.call(elements, formatter)
} 

document.addEventListener("DOMContentLoaded", function() {
  luxon.Settings.defaultLocale = 'cs'
  formatElement('.business-status', formatBusinessStatus)
  formatElement('.link-ext', formatExternalLink)
})
