// Open a vault with sgit.ai's vendored reader (assets/vendor/vault-embed.js, kept unmodified), for both layouts:
// the older one, where the head is the ref derived from the vault id, and the current one (sgit-ai 0.27 and on), where an
// encrypted branch index lists the branches and the named branch "current" points at its head ref. Uses only the reader's
// own methods (fileId, raw, decrypt, objJson, walk). Read keys only; nothing here can write. Apache-2.0.
(function () {
  'use strict'
  var dec = new TextDecoder()
  async function open(reader) {
    try { return await reader.open() } catch (legacy) {
      var idx = 'idx-pid-muw-' + await reader.fileId('sg-vault-v1:file-id:branch-index:' + reader.vaultId)
      var index
      try { index = JSON.parse(dec.decode(await reader.decrypt(await reader.raw('bare/indexes/' + idx)))) } catch (e) { throw legacy }
      var named = (index.branches || []).filter(function (b) { return b.branch_type === 'named' })
      var head = named.filter(function (b) { return b.name === 'current' })[0] || named[0]
      if (!head || !head.head_ref_id) throw new Error('the branch index names no head')
      var ref = JSON.parse(dec.decode(await reader.decrypt(await reader.raw('bare/refs/' + head.head_ref_id))))
      var commit = await reader.objJson(ref.commit_id)
      reader.files = {}
      await reader.walk(commit.tree_id, '')
      reader.branch = head.name
      return reader
    }
  }
  window.SGVaultOpen = open
})()
