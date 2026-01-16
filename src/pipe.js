// pipe server

import readline from 'readline'
import { stdout } from 'process'

import { ErrorNoCode, ErrorNoReturn, ErrorNoElement } from 'gum/error'
import { evaluateGum } from 'gum/eval'
import { renderPng } from 'gum/render'

const handlers = {
    evaluate: async (code, { size, theme }) => {
        const elem = evaluateGum(code, { size: size, theme })
        return elem.svg()
    },
    render: async (code, { size: size0, theme, background }) => {
        const elem = evaluateGum(code, { size: size0, theme })
        const svg = elem.svg()
        const { size } = elem
        const png0 = await renderPng(svg, { size, background })
        return png0.toString('base64')
    },
}

function parseError(e) {
    const { message } = e
    if (e instanceof ErrorNoCode) {
        return { error: 'NOCODE', message }
    } else if (e instanceof ErrorNoReturn) {
        return { error: 'NORETURN', message }
    } else if (e instanceof ErrorNoElement) {
        return { error: 'NOELEMENT', message }
    }
    return { error: 'PARSE', message }
}

// create readline interface
const rl = readline.createInterface({ input: process.stdin })

// handle lines from stdin
rl.on('line', async (line) => {
    const { task, code, size = 750, theme = 'light', background = 'white' } = JSON.parse(line)
    let message = null
    try {
        const result = await handlers[task](code, { size, theme, background })
        message = { ok: true, result }
    } catch (e) {
        const result = parseError(e)
        message = { ok: false, result }
    }
    stdout.write(JSON.stringify(message) + '\n')
})
