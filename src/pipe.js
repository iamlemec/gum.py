// pipe server

import readline from 'readline'
import { stdout } from 'process'

import { ErrorNoCode, ErrorNoReturn, ErrorNoElement } from 'gum-jsx/error'
import { evaluateGum } from 'gum-jsx/eval'

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
    const { code, ...args } = JSON.parse(line)
    let message = null
    try {
        const elem = evaluateGum(code, args)
        const result = elem.svg()
        message = { ok: true, result }
    } catch (e) {
        const result = parseError(e)
        message = { ok: false, result }
    }
    stdout.write(JSON.stringify(message) + '\n')
})
