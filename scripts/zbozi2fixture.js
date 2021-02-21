const {promises} = require('fs')
const {tagMap } = require('./tagMap')

async function readZbozi() {
  return JSON.parse(await promises.readFile('./zbozi.json'))
}

function slugify(name, aggr, attempt = 1) {
  const slugPart = name.toLowerCase().normalize('NFKD').replace(/[^\w\s-,]/g, '').replace(/[\s,]+/g, '-').replace(/-+/g, '-')
  const slug = `${slugPart}-${attempt}`
  const clash = aggr.find(item => item.fields.slug === slug)
  if (clash) {
    return slugify(name, aggr, attempt + 1)
  }
  return slug
}

function matches(obj, matcher) {
  return Object.entries(matcher).every(([field, value]) => obj[field] === value)
}

function getProductTag(row) {
  const match = tagMap.find(obj => matches(row, obj.match))

  if (match) {
    return match.data.tag
  } else {
    throw new Error(`No tag found for ${JSON.stringify(row, null, 2)}`)
  }
}

function transform(data) {
  const available = data.filter(row => Boolean(row.kodvyr) && row.show)
  const descriptions = []
  const usages = []
  const tags = []

  function createDescObj(data) {
    descriptions.push(data)
    return data
  }

  function createUsageObj(data) {
    usages.push(data)
    return data
  }

  function createTagObj(data) {
    tags.push(data)
    return data
  }

  const products = available.reduce((aggr, row) => {
    try {
      const tagObj = createTagObj({
        model: 'cajovyobchudek.ProductTag',
        pk: tags.length + 1,
        fields: {
          product: row.id,
          tag: getProductTag(row)
        }
      })
    } catch(e) {
      return aggr
    }
    const descObj = descriptions.find(item => item.fields.text === row.popis) || createDescObj({
      model: 'cajovyobchudek.ProductDescription',
      pk: descriptions.length + 1,
      fields: {
        text: row.popis,
        text_rendered: row.popis,
      }
    })
    const usageObj = usages.find(item => item.fields.text === row.pouziti) || createUsageObj({
      model: 'cajovyobchudek.ProductUsage',
      pk: usages.length + 1,
      fields: {
        text: row.pouziti,
        text_rendered: row.pouziti,
      }
    })

    return aggr.concat([{
      model: 'cajovyobchudek.Product',
      pk: row.id,
      fields: {
        name: row.nazev,
        slug: slugify(row.nazev, aggr),
        product_code: parseInt(row.kodvyr, 10),
        description: descObj.pk,
        usage: usageObj.pk,
      }
    }])
  }, [])

  return [...descriptions, ...usages, ...products, ...tags]
}

async function main() {
  const data = transform(await readZbozi())
  process.stdout.write(JSON.stringify(data, null, 2))
}

main()

