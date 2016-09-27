describe('ctx client', function() {
    describe('missing translation table', function() {
        it('refuses to apply transformations', function() {
            expect(CTX.process).toThrow();
        });
    });

    beforeEach(function() {
        document.body.insertAdjacentHTML(
            'afterbegin',
            '<div id="fixture"></div>'
        );
    });

    function installElement(html) {
        document.getElementById('fixture').innerHTML += html;
    }

    function installTranslationTable(json) {
        const fixture = '\
            <script type="application/json" id="ctx-permutations">\
               ' + json + '\
            </script>';

        installElement(fixture);
    }

    it('processes the trivial page', function() {
        installTranslationTable('[]');
        let before = document.body.innerHTML;
        CTX.process();
        let after = document.body.innerHTML;
        expect(before).toBe(after);
    });

    it('applies the identity transform', function() {
        installElement('<div id="test" data-ctx-origin="0">abc</div>');
        installTranslationTable('["abc"]');
        CTX.process();
        expect(document.getElementById('test').innerHTML).toBe('abc');
    });

    it('applies a simple transform', function() {
        installElement('<div id="test" data-ctx-origin="0">aaabbbccc</div>');
        installTranslationTable('["cba"]');
        CTX.process();
        expect(document.getElementById('test').innerHTML).toBe('cccbbbaaa');
    });

    afterEach(function() {
        document.body.removeElement(document.getElementById('fixture'));
    });
});
