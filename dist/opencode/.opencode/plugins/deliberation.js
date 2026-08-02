export const DeliberationPlugin = async ({ client }) => {
  await client?.app?.log?.({
    body: {
      service: "deliberation",
      level: "info",
      message: "Deliberation OpenCode plugin loaded. Invoke /deliberation for the work mode or /explain for a standalone explanation.",
      version: "0.1.0-dev.14",
    },
  })?.catch?.(() => undefined)

  return {}
}

export default DeliberationPlugin
