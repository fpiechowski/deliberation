export const DeliberationPlugin = async ({ client }) => {
  await client?.app?.log?.({
    body: {
      service: "deliberation",
      level: "info",
      message: "Deliberation OpenCode plugin loaded. Invoke /deliberation to activate the work mode.",
      version: "0.1.0-dev.10",
    },
  })?.catch?.(() => undefined)

  return {}
}

export default DeliberationPlugin
